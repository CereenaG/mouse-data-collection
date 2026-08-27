"""
Shared application state.

A single AppState instance is created in main.py and passed around to every
task screen and to the MouseLogger. It holds the one piece of information
that makes automatic labeling possible: `current_label`, which each task
screen updates the moment it becomes active.
"""

import os
from datetime import datetime


class AppState:
    def __init__(self, base_dir=None):
        self.participant_id = "unknown"
        self.current_task = "Idle"
        self.current_label = "Idle"
        self.session_start = datetime.now()

        # Root folder where all CSVs get written.
        self.base_dir = base_dir or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data"
        )
        self.base_dir = os.path.abspath(self.base_dir)
        os.makedirs(self.base_dir, exist_ok=True)

    def participant_dir(self):
        path = os.path.join(self.base_dir, f"participant_{self.participant_id}")
        os.makedirs(path, exist_ok=True)
        return path

    def set_task(self, task_name: str, label: str):
        self.current_task = task_name
        self.current_label = label

    def task_csv_path(self, task_name: str):
        safe_name = task_name.lower().replace(" ", "_")
        return os.path.join(self.participant_dir(), f"{safe_name}.csv")


# Module-level singleton, created lazily so every file can just do
# `from core.state import state`.
state = AppState()
