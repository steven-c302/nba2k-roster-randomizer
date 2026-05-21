"""
Converts a Kaggle NBA 2K ratings CSV into the players.json format used by this app.

Usage:
    python scripts/convert_csv.py

Edit the COLUMN_MAP below to match whichever CSV you downloaded.
Run with --inspect first to see the column names in your file.
"""

import csv
import json
import sys
from pathlib import Path

# --- Configure these to match your CSV's actual column headers ---
COLUMN_MAP = {
    "name":     "Player",    # player's full name
    "team":     "Team",      # NBA team name
    "position": "Position",  # primary position
    "overall":  "Overall",   # 2K overall rating (integer)
}

INPUT_PATH  = Path("data/nba2k_raw.csv")
OUTPUT_PATH = Path("data/players.json")

VALID_POSITIONS = {"PG", "SG", "SF", "PF", "C"}


def inspect(path: Path) -> None:
    """Print the first few rows so you can identify the right column names."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        print("Columns found in CSV:")
        for i, h in enumerate(headers):
            print(f"  [{i}] {h}")
        print("\nFirst 3 rows:")
        for i, row in enumerate(reader):
            if i >= 3:
                break
            print(dict(row))


def convert(input_path: Path, output_path: Path) -> None:
    players = []
    skipped = 0

    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                name     = row[COLUMN_MAP["name"]].strip()
                team     = row[COLUMN_MAP["team"]].strip()
                position = row[COLUMN_MAP["position"]].strip().upper()
                overall  = int(row[COLUMN_MAP["overall"]])
            except (KeyError, ValueError):
                skipped += 1
                continue

            # Keep only the first listed position if the CSV has combos like "PG/SG"
            position = position.split("/")[0].strip()

            if not name or not team or position not in VALID_POSITIONS:
                skipped += 1
                continue

            players.append({
                "name":     name,
                "team":     team,
                "position": position,
                "overall":  overall,
            })

    # Sort by overall descending so the file is easy to read
    players.sort(key=lambda p: p["overall"], reverse=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=2)

    print(f"Wrote {len(players)} players to {output_path}")
    if skipped:
        print(f"Skipped {skipped} rows (missing data or unrecognized position)")


if __name__ == "__main__":
    if "--inspect" in sys.argv:
        if not INPUT_PATH.exists():
            print(f"File not found: {INPUT_PATH}")
            sys.exit(1)
        inspect(INPUT_PATH)
        sys.exit(0)

    if not INPUT_PATH.exists():
        print(f"File not found: {INPUT_PATH}")
        print("Place your downloaded CSV at data/nba2k_raw.csv and try again.")
        sys.exit(1)

    convert(INPUT_PATH, OUTPUT_PATH)
