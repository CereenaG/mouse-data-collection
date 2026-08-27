from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal

from core.state import state


class WelcomeScreen(QWidget):
    start_requested = pyqtSignal()

    def __init__(self, task_names, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(18)

        title = QLabel("Mouse Interaction Data Collection")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "You'll be guided through a short sequence of tasks:\n"
            + " \u2192 ".join(task_names)
            + "\n\nEach task automatically labels your mouse movements, "
            "clicks, and timing - no manual annotation needed."
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addSpacing(10)
        id_label = QLabel("Participant ID:")
        id_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(id_label)

        self.id_input = QLineEdit()
        self.id_input.setAlignment(Qt.AlignCenter)
        self.id_input.setPlaceholderText("e.g. P01")
        layout.addWidget(self.id_input)

        self.start_button = QPushButton("Start")
        self.start_button.setFixedHeight(40)
        self.start_button.clicked.connect(self._on_start_clicked)
        layout.addWidget(self.start_button)

        layout.addStretch(1)

    def _on_start_clicked(self):
        participant_id = self.id_input.text().strip()
        if not participant_id:
            QMessageBox.warning(self, "Participant ID required", "Please enter a participant ID before starting.")
            return
        state.participant_id = participant_id
        self.start_requested.emit()
