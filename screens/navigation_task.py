import random

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

from screens.base_task import BaseTaskScreen


class _TargetCircle(QWidget):
    def __init__(self, on_reached, diameter=40, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        self.on_reached = on_reached

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#e74c3c"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.diameter, self.diameter)

    def enterEvent(self, event):
        self.on_reached()
        super().enterEvent(event)


class NavigationTaskScreen(BaseTaskScreen):
    task_name = "Navigation"
    label = "Navigation"
    instructions = "Move your cursor onto the red circle"
    repetitions_required = 8

    def build_task_ui(self, container: QWidget):
        self.container = container
        self.target = _TargetCircle(self._on_target_reached, parent=container)
        self.target.show()

    def reset_task(self):
        w = max(self.container.width() - 60, 100)
        h = max(self.container.height() - 60, 100)
        x = random.randint(0, w)
        y = random.randint(0, h)
        self.target.move(x, y)

    def _on_target_reached(self):
        self.mark_repetition_done(event_name="target_reached")
