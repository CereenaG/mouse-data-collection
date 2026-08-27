import random

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor

from screens.base_task import BaseTaskScreen


class _DragBox(QLabel):
    def __init__(self, on_dropped, on_drag_start, size=50, parent=None):
        super().__init__(parent)
        self.size = size
        self.setFixedSize(size, size)
        self.setStyleSheet(
            "background-color:#3498db; border-radius:6px;"
        )
        self.on_dropped = on_dropped
        self.on_drag_start = on_drag_start
        self._dragging = False
        self._drag_offset = QPoint(0, 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_offset = event.pos()
            self.on_drag_start()

    def mouseMoveEvent(self, event):
        if self._dragging:
            new_pos = self.mapToParent(event.pos() - self._drag_offset)
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if self._dragging:
            self._dragging = False
            self.on_dropped(self.geometry())


class _DropZone(QLabel):
    def __init__(self, size=70, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.setStyleSheet(
            "background-color: transparent; border: 3px dashed #9b59b6; border-radius:10px;"
        )


class DragTaskScreen(BaseTaskScreen):
    task_name = "Drag"
    label = "Drag"
    instructions = "Drag the blue box into the dashed target"
    repetitions_required = 6

    def build_task_ui(self, container: QWidget):
        self.container = container
        self.drop_zone = _DropZone(parent=container)
        self.box = _DragBox(
            on_dropped=self._on_dropped,
            on_drag_start=self._on_drag_start,
            parent=container,
        )
        self.drop_zone.show()
        self.box.show()
        self.box.raise_()

    def reset_task(self):
        w = self.container.width()
        h = self.container.height()

        zx = random.randint(0, max(w - self.drop_zone.width() - 40, 50)) + 20
        zy = random.randint(0, max(h - self.drop_zone.height() - 40, 50)) + 20
        self.drop_zone.move(zx, zy)

        bx = random.randint(0, max(w - self.box.width() - 40, 50)) + 20
        by = random.randint(0, max(h - self.box.height() - 40, 50)) + 20
        self.box.move(bx, by)
        self.box.raise_()

    def _on_drag_start(self):
        self.logger.log_event("drag_start")

    def _on_dropped(self, box_rect):
        if box_rect.intersects(self.drop_zone.geometry()):
            self.mark_repetition_done(event_name="drag_end_success")
        else:
            self.logger.log_event("drag_end_missed")
