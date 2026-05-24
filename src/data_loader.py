import json
from pathlib import Path


def load_players(file_path: str = "data/players.json") -> list[dict]:
    """Loads player data from a JSON file. Takes in an optional file path argument, which defaults to "data/players.json".
        Returns a list of player dictionaries."""
    data = Path(file_path)

    if not data.exists():
        raise FileNotFoundError(f"Could not find file: {file_path}")
    """checks if the specified file path exists. If it does not, a FileNotFoundError is raised with an appropriate error message."""
    with open(data, "r") as file:
        players = json.load(file)
    """opens the specified JSON file and loads the player data into a list of dictionaries."""

    return players