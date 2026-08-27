import random

from PyQt5.QtWidgets import QWidget, QPushButton, QMenu, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

from screens.base_task import BaseTaskScreen

MENU_TREE = {
    "File": ["New", "Open", "Save", "Export \u25b8"],
    "Edit": ["Undo", "Redo", "Cut", "Copy", "Paste"],
    "View": ["Zoom In", "Zoom Out", "Full Screen"],
}


class MenuTaskScreen(BaseTaskScreen):
    task_name = "MenuSelection"
    label = "Menu Selection"
    instructions = "Open the menu and select the requested item"
    repetitions_required = 6

    def build_task_ui(self, container: QWidget):
        self.container = container
        layout = QVBoxLayout(container)

        self.prompt = QLabel("")
        self.prompt.setStyleSheet("font-size: 14px; color:#2c3e50;")
        self.prompt.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.prompt)

        self.menu_button = QPushButton("Open Menu")
        self.menu_button.setFixedWidth(160)
        layout.addWidget(self.menu_button, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        self.menu_button.clicked.connect(self._open_menu)

    def reset_task(self):
        self._top = random.choice(list(MENU_TREE.keys()))
        self._item = random.choice(MENU_TREE[self._top])
        self.prompt.setText(f"Select:  {self._top} \u2192 {self._item}")

    def _open_menu(self):
        menu = QMenu(self)
        target_action = None
        for top_name, items in MENU_TREE.items():
            submenu = menu.addMenu(top_name)
            for item_name in items:
                action = submenu.addAction(item_name)
                if top_name == self._top and item_name == self._item:
                    target_action = action

        chosen = menu.exec_(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))
        if chosen is not None and chosen is target_action:
            self.mark_repetition_done(event_name="menu_item_selected_correct")
        elif chosen is not None:
            self.logger.log_event("menu_item_selected_wrong")
