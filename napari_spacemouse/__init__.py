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
    from napari_spacemouse import _napari

    if _spacemouse._active_device is not None:
        if device and _spacemouse._active_device.name != device:
            raise RuntimeError("Spacemouse already installed. Please uninstall first")
        _spacemouse.run()
        return

    if dev := _spacemouse.open(
        callback=_napari._apply_state_to_viewer,
        button_callback=_napari._handle_buttons,
        device=device,
    ):
        dev.run()


if __name__ == "__main__":
    import napari

    install()

    viewer = napari.Viewer(ndisplay=3)
    viewer.axes.visible = True

    viewer.open_sample("napari", "brain")
    # data = tuple(np.load(Path(__file__).parent / "wrench.npz").values())
    # viewer.add_surface(data)

    viewer.camera.angles = (0, 0, 0)
    napari.run()
