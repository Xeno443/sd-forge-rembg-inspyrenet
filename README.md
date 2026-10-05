# sd-forge-rembg-inspyrenet

InSPyReNet background removal for the Extras tab of [Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo).

It uses the [transparent-background](https://github.com/plemeri/transparent-background) library, the same one behind the ComfyUI Inspyrenet node.

It has been tested against Forge Neo 2.29.1. Other webuis are untested, and as usual this extension may break with later versions of Neo. Check for updates if you encounter any issues with this extension.

## Install

1. In the webui, open **Extensions → Install from URL**.
2. Paste `https://github.com/Xeno443/sd-forge-rembg-inspyrenet` and press **Install**.
3. Close the webui completely and start it again. The required packages are installed during that start.

The model weights (about 367 MB) are downloaded on first use.

## Use

Open the **Extras** tab and expand **InSPyReNet background removal**.

The network keeps the main subject of the image, usually the character(s), and removes everything else.

| Setting | What it does |
|---|---|
| Output: Transparent | The character(s) cut out, with a transparent background. |
| Output: Mask | Black-and-white mask: character(s) white, background black. |
| Output: White background | The character(s) on white. |
| Output: Custom color | The character(s) on a color you pick. |
| Threshold | At 0 the edges are soft and edge colors are cleaned up. Above 0 the cut is hard: every pixel is either fully kept or fully removed. |

Transparent output needs a file format that stores transparency, make sure the webui's image format is set to `png`, saving the result as `jpg` will remove the alpha channel. You can still use the color background options in that case.

## Where the weights go

The library stores them in a folder named `.transparent-background` in your user folder. If you already use the ComfyUI Inspyrenet node, the file is there and is not downloaded again.

For the license terms of the weights, see the upstream projects linked below.

## What gets installed

At startup the extension installs whichever of these are missing:

| Package | Note |
|---|---|
| `transparent-background` 1.3.4 | installed without its dependencies |
| `albumentations` 2.0.8 | installed without its dependencies |
| `albucore` 0.0.24 | installed without its dependencies |
| `timm`, `pymatting`, `easydict`, `gdown`, `wget`, `stringzilla`, `simsimd` | installed normally |

Nothing that is already installed is upgraded or replaced.

### Do not install opencv-python-headless

`albumentations` and `albucore` list `opencv-python-headless` as a requirement, which is why they are installed without dependencies: the webui already has OpenCV, and the headless package would overwrite it.

As a result, `pip check` reports that requirement as missing. That is expected. Do not install it to make the message go away. It replaces the webui's OpenCV build without warning, and uninstalling it afterwards leaves OpenCV broken until `opencv-python` is reinstalled.

## Credits

- InSPyReNet: <https://github.com/plemeri/InSPyReNet>
- transparent-background library (MIT, © 2022 Taehun Kim): <https://github.com/plemeri/transparent-background>
- ComfyUI node that prompted this extension: <https://github.com/john-mnz/ComfyUI-Inspyrenet-Rembg>
- Extras-tab pattern: <https://github.com/AUTOMATIC1111/stable-diffusion-webui-rembg>

## License

MIT, see [LICENSE](LICENSE).
