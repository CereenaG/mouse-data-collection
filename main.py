"""
Mouse Interaction Data Collection App
======================================

Guides a participant through a sequence of HCI-style micro-tasks
(navigation, clicking, dragging, precision selection, double-click, menu
selection, slider control, scrolling) while a background logger samples
cursor position/velocity/acceleration/button-state at ~100Hz and stamps
every row with the task that's currently active - so every sample is
automatically labeled, with zero manual annotation.

Run:
    python main.py
Output:
    data/participant_<ID>/<task>.csv   (one file per task)
    data/master_dataset.csv            (after clicking "Merge" on Finish screen,
                                         or via `python merge_data.py`)
"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from core.state import state
from core.logger import MouseLogger

from screens.welcome_screen import WelcomeScreen
from screens.finish_screen import FinishScreen
from screens.navigation_task import NavigationTaskScreen
from screens.click_task import ClickTaskScreen
from screens.drag_task import DragTaskScreen
from screens.precision_task import PrecisionTaskScreen
from screens.double_click_task import DoubleClickTaskScreen
from screens.menu_task import MenuTaskScreen
from screens.slider_task import SliderTaskScreen
from screens.scroll_task import ScrollTaskScreen

TASK_CLASSES = [
    NavigationTaskScreen,
    ClickTaskScreen,
    DragTaskScreen,
    PrecisionTaskScreen,
    DoubleClickTaskScreen,
    MenuTaskScreen,
    SliderTaskScreen,
    ScrollTaskScreen,
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse Interaction Data Collection")
        self.resize(900, 650)

        self.logger = MouseLogger(sample_hz=100)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        total = len(TASK_CLASSES)
        self.task_screens = [
            cls(self.logger, index=i + 1, total=total, parent=self)
            for i, cls in enumerate(TASK_CLASSES)
        ]

        self.welcome_screen = WelcomeScreen([cls.label for cls in TASK_CLASSES], parent=self)
        self.finish_screen = FinishScreen(parent=self)

        self.stack.addWidget(self.welcome_screen)          # index 0
        for screen in self.task_screens:
            self.stack.addWidget(screen)
        self.stack.addWidget(self.finish_screen)           # last index

        self.welcome_screen.start_requested.connect(self._start_session)
        for screen in self.task_screens:
            screen.task_complete.connect(self._advance)

    def _start_session(self):
        self.logger.start()
        self.stack.setCurrentWidget(self.task_screens[0])
        self.task_screens[0].on_enter()

    def _advance(self):
        current_index = self.stack.currentIndex()
        next_widget = self.stack.widget(current_index + 1)
        self.stack.setCurrentWidget(next_widget)

        if next_widget is self.finish_screen:
            self.logger.stop()
            self.finish_screen.on_enter()
        else:
            next_widget.on_enter()

    def closeEvent(self, event):
        self.logger.stop()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
