from modules import script_callbacks, scripts_postprocessing, ui_components
from backend import memory_management
import gradio as gr

from PIL import Image

outputs = ["Transparent", "Mask", "White background", "Custom color"]

vram_required = 4 * 1024**3

remover = None


def get_remover():
    global remover

    if remover is None:
        try:
            from transparent_background import Remover
        except ImportError as e:
            raise RuntimeError(f"InSPyReNet: could not load the transparent-background library ({e}). Restart the webui without --skip-install so the extension can install its packages.") from e

        remover = Remover(device="cpu")

    return remover


def unload_remover():
    global remover
    remover = None


script_callbacks.on_script_unloaded(unload_remover)


class ScriptPostprocessingInspyrenet(scripts_postprocessing.ScriptPostprocessing):
    name = "InSPyReNet"
    order = 20010

    def ui(self):
        with ui_components.InputAccordion(False, label="InSPyReNet background removal") as enable:
            with gr.Row():
                output = gr.Radio(label="Output", choices=outputs, value="Transparent")
                color = gr.ColorPicker(label="Background color", value="#00ff00", visible=False)

            threshold = gr.Slider(label="Threshold (0 = soft edges)", minimum=0.0, maximum=1.0, step=0.01, value=0.0)

            output.change(
                fn=lambda x: gr.update(visible=x == "Custom color"),
                inputs=[output],
                outputs=[color],
            )

        return {
            "enable": enable,
            "output": output,
            "color": color,
            "threshold": threshold,
        }

    def process(self, pp: scripts_postprocessing.PostprocessedImage, enable, output, color, threshold):
        if not enable:
            return

        remover = get_remover()

        device = memory_management.get_torch_device()
        memory_management.free_memory(vram_required, device)

        try:
            remover.model.to(device)
            remover.device = device
            image = remover.process(pp.image.convert("RGB"), type="rgba", threshold=threshold or None)
        finally:
            remover.model.to("cpu")
            remover.device = "cpu"
            memory_management.soft_empty_cache()

        if output == "Mask":
            image = image.getchannel("A").convert("RGB")
        elif output != "Transparent":
            background = Image.new("RGBA", image.size, "#ffffff" if output == "White background" else color)
            image = Image.alpha_composite(background, image).convert("RGB")

        pp.image = image
        pp.info["InSPyReNet"] = f"{output}, threshold {threshold}" if threshold else output
