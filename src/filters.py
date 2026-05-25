def filter_players_by_overall(players: list[dict], min_overall: int, max_overall: int) -> list[dict]:
    """Filters players by overall rating."""
    filtered_players = []

    for player in players:
        if min_overall <= player["overall"] <= max_overall:
            filtered_players.append(player)

    return filtered_players


def filter_players_by_position(players: list[dict], positions: list[str]) -> list[dict]:
    """Filters players by position."""
    filtered_players = []

    for player in players:
        if player["position"] in positions:
            filtered_players.append(player)

    return filtered_players
