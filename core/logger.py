"""
MouseLogger

Samples cursor position at a fixed rate (default ~100 Hz) and writes one CSV
row per sample: Time, ParticipantID, Task, Label, X, Y, Velocity,
Acceleration, ButtonState, ActiveWindow, Event.

`Label` is read from the shared AppState on every tick, so whichever task
screen is currently active automatically stamps every row it produces -
this is the "no manual work needed" auto-labeling described in the design.

Discrete events (a click landing on a target, a drag starting/ending, a
menu item chosen, etc.) are written immediately via log_event() with the
Event column filled in, instead of waiting for the next timer tick.
"""

import csv
import os
import time

from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from core.state import state
from core import ui_context

CSV_HEADER = [
    "Time",
    "ParticipantID",
    "Task",
    "Label",
    "X",
    "Y",
    "Velocity",
    "Acceleration",
    "ButtonState",
    "ActiveWindow",
    "Event",
]


class MouseLogger(QObject):
    def __init__(self, sample_hz: int = 100, parent=None):
        super().__init__(parent)
        self.interval_ms = max(1, int(1000 / sample_hz))
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

        self._prev_pos = None
        self._prev_time = None
        self._prev_velocity = 0.0

        self._current_file = None
        self._current_writer = None
        self._current_task_name = None

        self._start_time = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def start(self):
        self._start_time = time.time()
        self._prev_pos = QCursor.pos()
        self._prev_time = self._start_time
        self._prev_velocity = 0.0
        self._timer.start(self.interval_ms)

    def stop(self):
        self._timer.stop()
        self._close_current_file()

    def _open_file_for_task(self, task_name: str):
        """Switch the CSV file being written to when the active task
        changes. Each task gets its own file, e.g. navigation.csv,
        click.csv, matching the layout in the design doc."""
        if task_name == self._current_task_name:
            return
        self._close_current_file()

        path = state.task_csv_path(task_name)
        is_new = not os.path.exists(path)
        self._current_file = open(path, "a", newline="", encoding="utf-8")
        self._current_writer = csv.writer(self._current_file)
        if is_new:
            self._current_writer.writerow(CSV_HEADER)
        self._current_task_name = task_name

    def _close_current_file(self):
        if self._current_file is not None:
            self._current_file.flush()
            self._current_file.close()
            self._current_file = None
            self._current_writer = None
            self._current_task_name = None

    # ------------------------------------------------------------------
    # Sampling
    # ------------------------------------------------------------------
    def _tick(self):
        now = time.time()
        pos = QCursor.pos()

        dt = max(now - self._prev_time, 1e-6)
        dx = pos.x() - self._prev_pos.x()
        dy = pos.y() - self._prev_pos.y()
        distance = (dx ** 2 + dy ** 2) ** 0.5
        velocity = distance / dt
        acceleration = (velocity - self._prev_velocity) / dt

        button_state = self._button_state_string()
        active_window = ui_context.get_active_window_title()

        self._write_row(
            t=now - self._start_time,
            x=pos.x(),
            y=pos.y(),
            velocity=velocity,
            acceleration=acceleration,
            button_state=button_state,
            active_window=active_window,
            event="",
        )

        self._prev_pos = pos
        self._prev_time = now
        self._prev_velocity = velocity

    def _button_state_string(self):
        buttons = QApplication.mouseButtons()
        pressed = []
        if buttons & Qt.LeftButton:
            pressed.append("Left")
        if buttons & Qt.RightButton:
            pressed.append("Right")
        if buttons & Qt.MiddleButton:
            pressed.append("Middle")
        return "+".join(pressed) if pressed else "None"

    # ------------------------------------------------------------------
    # Public API used by task screens
    # ------------------------------------------------------------------
    def log_event(self, event_name: str):
        """Write an immediate row for a discrete event, e.g. 'click_target',
        'drag_start', 'drag_end', 'double_click', 'menu_item_selected',
        'slider_released', 'scroll_item_selected'."""
        now = time.time()
        pos = QCursor.pos()
        self._write_row(
            t=now - self._start_time,
            x=pos.x(),
            y=pos.y(),
            velocity=self._prev_velocity,
            acceleration=0.0,
            button_state=self._button_state_string(),
            active_window=ui_context.get_active_window_title(),
            event=event_name,
        )

    def _write_row(self, t, x, y, velocity, acceleration, button_state, active_window, event):
        self._open_file_for_task(state.current_task)
        self._current_writer.writerow(
            [
                f"{t:.4f}",
                state.participant_id,
                state.current_task,
                state.current_label,
                x,
                y,
                f"{velocity:.2f}",
                f"{acceleration:.2f}",
                button_state,
                active_window,
                event,
            ]
        )
        # Flush regularly so a crash doesn't lose the whole session.
        self._current_file.flush()
