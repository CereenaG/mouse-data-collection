import random

from PyQt5.QtWidgets import QWidget, QPushButton

from screens.base_task import BaseTaskScreen


class PrecisionTaskScreen(BaseTaskScreen):
    task_name = "PrecisionSelection"
    label = "Precision Selection"
    instructions = "Click the tiny target (it's small on purpose!)"
    repetitions_required = 8

    def build_task_ui(self, container: QWidget):
        self.container = container
        self.button = QPushButton("", parent=container)
        self.button.setStyleSheet(
            "background-color:#e67e22; border-radius:3px;"
        )
        self.button.clicked.connect(self._on_clicked)
        self.button.show()

    def reset_task(self):
        size = random.randint(15, 20)
        self.button.setFixedSize(size, size)
        w = max(self.container.width() - size, 100)
        h = max(self.container.height() - size, 100)
        x = random.randint(0, w)
        y = random.randint(0, h)
        self.button.move(x, y)

    def _on_clicked(self):
        self.mark_repetition_done(event_name="precision_click")
