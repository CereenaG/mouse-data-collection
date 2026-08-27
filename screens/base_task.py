from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import pyqtSignal, Qt

from core.state import state


class BaseTaskScreen(QWidget):
    """Common scaffolding for every task screen.

    Subclasses must set `task_name` and `label` and implement
    `build_task_ui(layout)` and `reset_task()`. Call `self.mark_repetition_done()`
    each time one repetition of the task is completed; once
    `repetitions_required` is reached, `task_complete` fires automatically.
    """

    task_complete = pyqtSignal()

    task_name = "Task"
    label = "Task"
    instructions = "Follow the on-screen instructions."
    repetitions_required = 5

    def __init__(self, logger, index, total, parent=None):
        super().__init__(parent)
        self.logger = logger
        self.index = index
        self.total = total
        self.repetitions_done = 0

        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(30, 20, 30, 20)

        header = QLabel(f"Task {self.index} / {self.total}  \u2014  {self.instructions}")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.outer_layout.addWidget(header)

        self.progress = QProgressBar()
        self.progress.setRange(0, self.repetitions_required)
        self.progress.setValue(0)
        self.outer_layout.addWidget(self.progress)

        self.task_area = QWidget()
        self.outer_layout.addWidget(self.task_area, stretch=1)

        self.build_task_ui(self.task_area)

    def on_enter(self):
        """Called by MainWindow every time this screen becomes visible."""
        state.set_task(self.task_name, self.label)
        self.repetitions_done = 0
        self.progress.setValue(0)
        self.reset_task()

    def mark_repetition_done(self, event_name: str = ""):
        if event_name:
            self.logger.log_event(event_name)
        self.repetitions_done += 1
        self.progress.setValue(self.repetitions_done)
        if self.repetitions_done >= self.repetitions_required:
            self.task_complete.emit()
        else:
            self.reset_task()

    # ------------------------------------------------------------------
    # Overridden by subclasses
    # ------------------------------------------------------------------
    def build_task_ui(self, container: QWidget):
        raise NotImplementedError

    def reset_task(self):
        """Set up the next repetition (move target, pick new value, etc.)."""
        raise NotImplementedError
