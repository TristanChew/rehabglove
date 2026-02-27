import os
import re
from collections import defaultdict

# =========================
# CONFIG
# =========================
DATA_FOLDER = "DATA"
VIDEO_FOLDER = "VIDEO"
MAX_CSV = 30
MAX_VIDEO_DATES = 3


# =========================
# CLEAN CSV FILES
# =========================
def clean_csv():
    if not os.path.exists(DATA_FOLDER):
        return

    pattern = re.compile(r"^(\d{8})_DATA\.csv$")
    files = []

    for f in os.listdir(DATA_FOLDER):
        match = pattern.match(f)
        if match:
            files.append(f)

    files.sort()  # Oldest first (YYYYMMDD format)

    if len(files) > MAX_CSV:
        to_delete = files[:len(files) - MAX_CSV]
        for f in to_delete:
            os.remove(os.path.join(DATA_FOLDER, f))
            print(f"Deleted CSV: {f}")


# =========================
# CLEAN VIDEO FILES
# =========================
def clean_video():
    if not os.path.exists(VIDEO_FOLDER):
        return

    pattern = re.compile(r"^(\d{8})_VIDEO_\d+\.mp4$")
    videos_by_date = defaultdict(list)

    for f in os.listdir(VIDEO_FOLDER):
        match = pattern.match(f)
        if match:
            date = match.group(1)
            videos_by_date[date].append(f)

    dates = sorted(videos_by_date.keys())  # Oldest first

    if len(dates) > MAX_VIDEO_DATES:
        dates_to_delete = dates[:len(dates) - MAX_VIDEO_DATES]

        for date in dates_to_delete:
            for f in videos_by_date[date]:
                os.remove(os.path.join(VIDEO_FOLDER, f))
                print(f"Deleted Video: {f}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    clean_csv()
    clean_video()
