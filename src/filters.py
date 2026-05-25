def filter_players_by_overall(players: list[dict], min_overall: int, max_overall: int) -> list[dict]:
    """Filters players by overall rating. Takes in inputs of a list of players, a minimum overall rating, and a maximum overall rating. 
    Returns a list of players that fall within the specified overall rating range."""
    filtered_players = []
    """sets up an empty list to store the filtered players"""
    for player in players:
        if min_overall <= player["overall"] <= max_overall:
            filtered_players.append(player)
    """iterates through each player in the input list and checks if their overall rating falls within the specified range.
    If it does, the player is added to the filtered_players list."""
    return filtered_players


def filter_players_by_position(players: list[dict], positions: list[str]) -> list[dict]:
    """Filters players by position."""
    filtered_players = []

    for player in players:
        if player["position"] in positions:
            filtered_players.append(player)
    return filtered_players