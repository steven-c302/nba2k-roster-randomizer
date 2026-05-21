import random


def create_random_rosters(
    users: list[str],
    players: list[dict],
    team_size: int
) -> dict[str, list[dict]] | None:
    """
    Randomly creates a roster for each user.

    Each NBA player can only be selected once.
    """
    total_players_needed = len(users) * team_size

    if total_players_needed > len(players):
        return None

    chosen_players = random.sample(players, total_players_needed)

    rosters = {}

    current_index = 0

    for user in users:
        user_roster = chosen_players[current_index:current_index + team_size]
        rosters[user] = user_roster
        current_index += team_size

    return rosters