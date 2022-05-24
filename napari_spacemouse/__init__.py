from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("napari-spacemouse")
except PackageNotFoundError:
    __version__ = "unknown"

__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"


from napari_spacemouse import _spacemouse


def uninstall():
    _spacemouse.stop()


def install(device: str = None):
    """patch napari to be spacemouse aware."""
    from napari_spacemouse._napari import _apply_state_to_viewer

    if _spacemouse._active_device is not None:
        if device and _spacemouse._active_device.name != device:
            raise RuntimeError("Spacemouse already installed. Please uninstall first")
        _spacemouse.run()
        return

    if dev := _spacemouse.open(callback=_apply_state_to_viewer, device=device):
        dev.run()


if __name__ == "__main__":
    import napari
    import numpy as np
    from pathlib import Path

    install()

    data = tuple(np.load(Path(__file__).parent / "wrench.npz").values())

    viewer = napari.Viewer(ndisplay=3)
    viewer.add_surface(data)

    napari.run()

# troubleshoot
# start with (0,0,0) -> (Y+clockwise, Z+clockwise, X+clockwise)
# rotate each axis, evaluate what it moves in the image.

# right-handed rotation, rotating counter-clockwise when looking at zero from positive

# tilt away from me -> pitch goes up
# rotate (doorknob) clockwise -> yaw goes up
# tilt right -> roll goes up
