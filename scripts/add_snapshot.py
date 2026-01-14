import csv
from datetime import datetime
from pathlib import Path
import argparse

DATA_PATH = Path("data/post_timeseries.csv")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--impressions", type=int, required=True)
    parser.add_argument("--reactions", type=int, required=True)
    parser.add_argument("--comments", type=int, required=True)
    parser.add_argument("--shares", type=int, required=True)
    args = parser.parse_args()

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = DATA_PATH.exists()

    with DATA_PATH.open("a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "impressions", "reactions", "comments", "shares"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), args.impressions, args.reactions, args.comments, args.shares])

    print(f"✅ Snapshot añadido: {DATA_PATH}")

if __name__ == "__main__":
    main()

