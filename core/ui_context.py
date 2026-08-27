"""
Best-effort Windows UI Automation context.

On Windows, with pywin32 (and optionally `uiautomation`) installed, this
grabs the foreground window title and, if available, a short description
of the control under the cursor (e.g. "Button 'CLICK'"). This gives the
semantic context mentioned in the design doc (Button/Menu/Textbox/etc.)

On any platform where those libraries aren't available (e.g. while you're
developing on the Linux side of your dual-boot before testing on Windows),
every function here quietly falls back to "N/A" instead of crashing, so the
rest of the app keeps working.
"""

_win32_available = False
_uia_available = False

try:
    import win32gui  # type: ignore

    _win32_available = True
except Exception:
    win32gui = None

try:
    import uiautomation as auto  # type: ignore

    _uia_available = True
except Exception:
    auto = None


def get_active_window_title() -> str:
    if not _win32_available:
        return "N/A"
    try:
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd) or "N/A"
    except Exception:
        return "N/A"


def get_control_under_cursor(x: int, y: int) -> str:
    """Returns a short description like "Button 'CLICK'" if the
    `uiautomation` package is installed. Otherwise returns "N/A".
    """
    if not _uia_available:
        return "N/A"
    try:
        control = auto.ControlFromPoint(x, y)
        if control is None:
            return "N/A"
        ctrl_type = getattr(control, "ControlTypeName", "Control")
        name = getattr(control, "Name", "") or ""
        return f"{ctrl_type} '{name}'".strip()
    except Exception:
        return "N/A"
