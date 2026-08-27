from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

from core.state import state
from merge_data import merge_participant_csvs


class FinishScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(18)

        title = QLabel("All done \u2705")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.info = QLabel("")
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setWordWrap(True)
        layout.addWidget(self.info)

        merge_button = QPushButton("Merge this participant's CSVs into master_dataset.csv")
        merge_button.clicked.connect(self._on_merge_clicked)
        layout.addWidget(merge_button)

        layout.addStretch(1)

    def on_enter(self):
        self.info.setText(
            f"Thanks! Data for participant '{state.participant_id}' has been saved to:\n"
            f"{state.participant_dir()}"
        )

    def _on_merge_clicked(self):
        try:
            out_path = merge_participant_csvs(state.base_dir)
            QMessageBox.information(self, "Merged", f"Master dataset written to:\n{out_path}")
        except Exception as exc:
            QMessageBox.critical(self, "Merge failed", str(exc))
