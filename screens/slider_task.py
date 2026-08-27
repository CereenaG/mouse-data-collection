import random

from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

from screens.base_task import BaseTaskScreen

TOLERANCE = 2


class SliderTaskScreen(BaseTaskScreen):
    task_name = "SliderControl"
    label = "Slider Control"
    instructions = "Drag the slider to match the target value"
    repetitions_required = 6

    def build_task_ui(self, container: QWidget):
        self.container = container
        layout = QVBoxLayout(container)

        self.prompt = QLabel("")
        self.prompt.setAlignment(Qt.AlignCenter)
        self.prompt.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.prompt)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderReleased.connect(self._on_released)
        layout.addWidget(self.slider)
        layout.addStretch(1)

    def reset_task(self):
        self._target = random.randint(10, 90)
        self.slider.setValue(random.randint(0, 100))
        self.prompt.setText(f"Target value: {self._target}")

    def _on_released(self):
        value = self.slider.value()
        if abs(value - self._target) <= TOLERANCE:
            self.mark_repetition_done(event_name="slider_released_correct")
        else:
            self.logger.log_event("slider_released_missed")
