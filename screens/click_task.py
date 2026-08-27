import random

from PyQt5.QtWidgets import QWidget, QPushButton

from screens.base_task import BaseTaskScreen


class ClickTaskScreen(BaseTaskScreen):
    task_name = "Click"
    label = "Click"
    instructions = "Click the highlighted button"
    repetitions_required = 8

    def build_task_ui(self, container: QWidget):
        self.container = container
        self.button = QPushButton("CLICK", parent=container)
        self.button.setFixedSize(120, 50)
        self.button.setStyleSheet(
            "background-color:#2ecc71; color:white; font-weight:bold; border-radius:8px;"
        )
        self.button.clicked.connect(self._on_clicked)
        self.button.show()

    def reset_task(self):
        w = max(self.container.width() - self.button.width(), 100)
        h = max(self.container.height() - self.button.height(), 100)
        x = random.randint(0, w)
        y = random.randint(0, h)
        self.button.move(x, y)

    def _on_clicked(self):
        self.mark_repetition_done(event_name="click_target")
