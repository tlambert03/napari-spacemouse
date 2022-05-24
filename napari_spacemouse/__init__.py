try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"

from typing import TYPE_CHECKING, Optional
import threading

if TYPE_CHECKING:
    from ._spacemouse import MouseState

_THREAD: Optional["StoppableThread"] = None


def uninstall():
    global _THREAD
    if _THREAD:
        _THREAD.stop()
        _THREAD.join()
        _THREAD = None
        print("done")


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, dev, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dev = dev
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            try:
                self._dev.read()
            except OSError:
                return
        self._dev.close()


def install() -> bool:
    """patch napari to be spacemouse aware."""
    from napari.viewer import current_viewer
    from napari_spacemouse._spacemouse import open

    global _THREAD

    def _callback(state: "MouseState"):
        if v := current_viewer():
            if v.dims.ndisplay == 3:
                rpy = (-state.yaw, -state.roll, state.pitch)
                v.camera.angles = tuple(a + b for a, b in zip(v.camera.angles, rpy))

    if dev := open(callback=_callback):
        _THREAD = StoppableThread(dev)
        _THREAD.start()
        return True
    return False


if __name__ == "__main__":
    import napari

    viewer = napari.Viewer(ndisplay=3)
    viewer.open_sample("napari", "brain")
    install()
    napari.run()
