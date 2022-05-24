import numpy as np
from scipy.spatial.transform import Rotation as R
from napari.utils.events import EventedModel
from . import _spacemouse as sm


class Config(EventedModel):
    roll_active: bool = True
    pitch_active: bool = True
    yaw_active: bool = True
    zoom_active: bool = True
    x_active: bool = True
    z_active: bool = True
    gain_zoom: float = 1
    gain_roll: float = 1
    gain_pitch: float = 1
    gain_yaw: float = 1


CFG = Config()


def _apply_state_to_viewer(s: sm.MouseState, v=None):
    from napari.viewer import current_viewer

    v = v or current_viewer()
    if not v:
        return
    if all(s.buttons):
        v.reset_view()
        return

    if v.dims.ndisplay == 3:
        # lower-case is extrinsic, uppercase is intrinsic

        cam = R.from_euler("yzx", v.camera.angles, True)

        p = s.pitch if CFG.pitch_active else 0
        r = s.roll if CFG.roll_active else 0
        y = s.yaw if CFG.yaw_active else 0
        rot = R.from_euler("XYZ", (-p, r, -y), True)

        T = cam.as_matrix() @ rot.inv().as_matrix()  # all messed up, i know

        v.camera.angles = R.from_matrix(T).as_euler("yzx", True)

        # TODO: needs extrinsic coords
        v.camera.center = np.array(v.camera.center) + np.array((0, s.z, -s.x))

        if s.buttons[1]:
            v.camera.perspective = max(0, min(v.camera.perspective + s.y, 90))
        elif CFG.zoom_active:
            v.camera.zoom = v.camera.zoom - s.y * CFG.gain_zoom / 10
