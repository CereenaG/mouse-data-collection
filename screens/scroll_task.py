import random

from PyQt5.QtWidgets import QWidget, QListWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

from screens.base_task import BaseTaskScreen

NUM_ITEMS = 80


class ScrollTaskScreen(BaseTaskScreen):
    task_name = "Scroll"
    label = "Scroll"
    instructions = "Scroll the list and click the requested item"
    repetitions_required = 5

    def build_task_ui(self, container: QWidget):
        self.container = container
        layout = QVBoxLayout(container)

        self.prompt = QLabel("")
        self.prompt.setAlignment(Qt.AlignCenter)
        self.prompt.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.prompt)

        self.list_widget = QListWidget()
        for i in range(1, NUM_ITEMS + 1):
            self.list_widget.addItem(f"Item {i:03d}")
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.list_widget, stretch=1)

    def reset_task(self):
        self._target_index = random.randint(1, NUM_ITEMS)
        self.prompt.setText(f"Find and click:  Item {self._target_index:03d}")
        self.list_widget.scrollToTop()
        self.list_widget.clearSelection()

    def _on_item_clicked(self, item):
        if item.text() == f"Item {self._target_index:03d}":
            self.mark_repetition_done(event_name="scroll_item_selected_correct")
        else:
            self.logger.log_event("scroll_item_selected_wrong")
