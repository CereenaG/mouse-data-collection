"""
Merge every participant_*/*.csv file produced by the app into a single
master_dataset.csv sitting next to the participant folders.

Can be run standalone:
    python merge_data.py [data_dir]
or called from the Finish screen inside the app.
"""

import csv
import os
import sys
import glob


def merge_participant_csvs(data_dir: str) -> str:
    csv_files = sorted(glob.glob(os.path.join(data_dir, "participant_*", "*.csv")))
    if not csv_files:
        raise FileNotFoundError(f"No per-task CSV files found under {data_dir}")

    out_path = os.path.join(data_dir, "master_dataset.csv")
    header_written = False

    with open(out_path, "w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        for path in csv_files:
            with open(path, "r", newline="", encoding="utf-8") as in_file:
                reader = csv.reader(in_file)
                rows = list(reader)
                if not rows:
                    continue
                if not header_written:
                    writer.writerow(rows[0])
                    header_written = True
                writer.writerows(rows[1:])

    return out_path


if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data"
    )
    result_path = merge_participant_csvs(target_dir)
    print(f"Master dataset written to: {result_path}")
