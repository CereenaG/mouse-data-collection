import random

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt

from screens.base_task import BaseTaskScreen


class _Icon(QLabel):
    def __init__(self, on_double_clicked, parent=None):
        super().__init__("\U0001F4C1", parent)  # folder emoji as a stand-in icon
        self.setStyleSheet("font-size: 36px;")
        self.setFixedSize(60, 60)
        self.setAlignment(Qt.AlignCenter)
        self.on_double_clicked = on_double_clicked

    def mouseDoubleClickEvent(self, event):
        self.on_double_clicked()


class DoubleClickTaskScreen(BaseTaskScreen):
    task_name = "DoubleClick"
    label = "Double Click"
    instructions = "Double-click the folder icon to open it"
    repetitions_required = 6

    def build_task_ui(self, container: QWidget):
        self.container = container
        self.icon = _Icon(self._on_double_clicked, parent=container)
        self.icon.show()

    def reset_task(self):
        w = max(self.container.width() - self.icon.width(), 100)
        h = max(self.container.height() - self.icon.height(), 100)
        x = random.randint(0, w)
        y = random.randint(0, h)
        self.icon.move(x, y)

    def _on_double_clicked(self):
        self.mark_repetition_done(event_name="double_click")
