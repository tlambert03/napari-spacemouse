from qtpy import QtWidgets as QtW

from . import _spacemouse as sm
from . import install, uninstall
from ._napari import CFG


class SpaceMouse(QtW.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._dev_combo = QtW.QComboBox()
        self._dev_combo.addItems(sm.list_connected_devices())

        self._on_btn = QtW.QPushButton()
        self._on_btn.setCheckable(True)
        self._on_btn.toggled.connect(self._on_btn_changed)
        # running = bool(sm._active_device and sm._active_device.is_running)
        self._on_btn.setChecked(True)
        self._on_btn_changed(True)

        self.setLayout(QtW.QVBoxLayout())
        self.layout().addWidget(self._dev_combo)
        self.layout().addWidget(self._on_btn)

        # needs magicgui from pydantic model
        for name, field in CFG.__fields__.items():
            if field.type_ is bool:
                box = QtW.QCheckBox(name)
                box.setChecked(getattr(CFG, name))
                box.setObjectName(name)
                box.toggled.connect(self._cfg_toggled)
                self.layout().addWidget(box)

    def _on_btn_changed(self, state: bool):
        if state:
            self._on_btn.setText("Deactivate Mouse")
            self._on_btn.setStyleSheet("background-color: #A00")
            install(self._dev_combo.currentText())
        else:
            self._on_btn.setText("Activate Mouse")
            self._on_btn.setStyleSheet("")
            uninstall()

    def _cfg_toggled(self, state):

        setattr(CFG, self.sender().objectName(), state)
