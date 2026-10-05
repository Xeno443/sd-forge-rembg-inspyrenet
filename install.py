import launch

# Installed without their dependencies: albumentations and albucore ask for
# opencv-python-headless, which would overwrite the OpenCV the webui already has.
pinned_no_deps = [
    "transparent-background==1.3.4",
    "albumentations==2.0.8",
    "albucore==0.0.24",
]

packages = ["timm", "pymatting", "easydict", "gdown", "wget", "stringzilla", "simsimd"]

for spec in pinned_no_deps:
    name = spec.split("==")[0]
    if not launch.is_installed(name):
        launch.run_pip(f"install --no-deps {spec}", f"{name} for InSPyReNet extension")

for name in packages:
    if not launch.is_installed(name):
        launch.run_pip(f"install {name}", f"{name} for InSPyReNet extension")
