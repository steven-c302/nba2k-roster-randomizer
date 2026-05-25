import random


def create_random_rosters(users: list[str], players: list[dict], team_size: int) -> dict[str, list[dict]] | None:
    """Randomly creates a roster for each user. Each NBA player can only be selected once.
    Takes in a list of user names, a list of player dictionaries, and a team size (number of players per roster).
    Returns a dictionary where each key is a user name and the corresponding value is a list of
    player dictionaries representing that user's roster. If there are not enough players to create the rosters, returns None."""

    total_players_needed = len(users) * team_size

    if total_players_needed > len(players):
        return None

    required_positions = ["PG", "SG", "SF", "PF", "C"]

    rosters = {}

    for user in users:
        rosters[user] = []

    available_players = players.copy()

    for position in required_positions:
        players_at_position = []

        for player in available_players:
            if player["position"] == position:
                players_at_position.append(player)

        if len(players_at_position) < len(users):
            print(f"Not enough players at position: {position}")
            return None

        chosen_players = random.sample(players_at_position, len(users))

        for index, user in enumerate(users):
            selected_player = chosen_players[index]
            rosters[user].append(selected_player)
            available_players.remove(selected_player)

    return rosters