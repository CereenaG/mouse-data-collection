# Mouse Interaction Data Collection App

A PyQt5 desktop application that guides a participant through 8 HCI-style
micro-tasks while a background logger records mouse behavior — every sample
is **automatically labeled** with the task that was active, so there's no
manual annotation step.

## Tasks included

1. **Navigation** — move the cursor onto a moving target circle
2. **Click** — click a button at random positions
3. **Drag** — drag a box into a target zone
4. **Precision Selection** — click a tiny (15–20px) target
5. **Double Click** — double-click a folder icon
6. **Menu Selection** — navigate a cascading menu to a requested item
7. **Slider Control** — drag a slider to match a target value
8. **Scroll** — scroll a long list and click a specific item

## Setup

```bash
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

`pywin32` and `uiautomation` are optional and Windows-only — they enable
capturing the real active window title and the control under the cursor
(Button/Menu/Textbox/etc). Without them (e.g. testing on the Linux side of
a dual-boot setup) those columns just read `"N/A"` and everything else
still works.

## Run

```bash
python main.py
```

Enter a participant ID, click **Start**, and work through the 8 tasks.

## Output

```
data/
  participant_<ID>/
    navigation.csv
    click.csv
    drag.csv
    precisionselection.csv
    doubleclick.csv
    menuselection.csv
    slidercontrol.csv
    scroll.csv
  master_dataset.csv   (created after clicking "Merge" on the Finish screen,
                         or by running `python merge_data.py`)
```

### CSV schema

| Column | Meaning |
|---|---|
| Time | Seconds since the session started |
| ParticipantID | ID entered on the welcome screen |
| Task | Which task screen was active |
| Label | Same as Task — the ML training label |
| X, Y | Cursor position (screen coordinates) |
| Velocity | px/sec, derived from consecutive samples |
| Acceleration | change in velocity per second |
| ButtonState | `None`, `Left`, `Right`, `Middle`, or combinations |
| ActiveWindow | Foreground window title (Windows-only, else `N/A`) |
| Event | Filled in for discrete events, e.g. `target_reached`, `drag_start`, `drag_end_success`, `click_target`, `menu_item_selected_correct` — blank on ordinary background samples |

Sampling rate defaults to ~100Hz (`MouseLogger(sample_hz=100)` in `main.py`).

## Project layout

```
main.py                 — entry point, MainWindow / screen flow
merge_data.py            — merges all participant CSVs into master_dataset.csv
core/
  state.py               — shared AppState (participant id, current label)
  logger.py               — MouseLogger: sampling + CSV writing
  ui_context.py            — best-effort Windows UI Automation helpers
screens/
  base_task.py             — shared scaffolding (progress bar, repetitions)
  welcome_screen.py, finish_screen.py
  navigation_task.py, click_task.py, drag_task.py, precision_task.py,
  double_click_task.py, menu_task.py, slider_task.py, scroll_task.py
```

## Extending it

- Adjust `repetitions_required` on any task screen to collect more/less data per task.
- Add a new task by subclassing `BaseTaskScreen` (see any existing task for the pattern) and adding it to `TASK_CLASSES` in `main.py`.
- Sampling rate: change `MouseLogger(sample_hz=100)` in `main.py`.
