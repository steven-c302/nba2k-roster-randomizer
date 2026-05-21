import json
from pathlib import Path


def load_players(file_path: str = "data/players.json") -> list[dict]:
    """
    Loads NBA player data from a JSON file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Could not find file: {file_path}")

    with open(path, "r") as file:
        players = json.load(file)

    return players