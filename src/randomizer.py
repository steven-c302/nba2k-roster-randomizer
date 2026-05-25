import random


def create_rosters_with_starters(
    users: list[str],
    players: list[dict],
    team_size: int
) -> dict[str, dict[str, list[dict]]] | None:
    """
    Creates a roster for each user.

    Each roster has:
    - 5 starters: PG, SG, SF, PF, C
    - Optional bench players if team_size is greater than 5

    The full roster is generated first.
    Then the best player at each required position becomes the starter.
    Everyone else becomes bench.

    Each NBA player can only be selected once.
    """
    required_positions = ["PG", "SG", "SF", "PF", "C"]

    if team_size < 5 or team_size > 15:
        print("Team size must be between 5 and 15.")
        return None

    total_players_needed = len(users) * team_size

    if total_players_needed > len(players):
        print("Not enough total players available.")
        return None

    rosters = {user: [] for user in users}
    available_players = players.copy()

    # Step 1: distribute one player per position to all users before moving to next position
    for position in required_positions:
        players_at_position = [p for p in available_players if p["position"] == position]

        if len(players_at_position) < len(users):
            print(f"Not enough players available at position: {position}")
            return None

        chosen = random.sample(players_at_position, len(users))

        for user, player in zip(users, chosen):
            rosters[user].append(player)
            available_players.remove(player)

    # Step 2: fill remaining bench spots for all users
    bench_spots_needed = team_size - 5

    for user in users:
        if len(available_players) < bench_spots_needed:
            print("Not enough players available for bench spots.")
            return None

        extra_players = random.sample(available_players, bench_spots_needed)

        for player in extra_players:
            rosters[user].append(player)
            available_players.remove(player)

    for user in users:
        user_roster = rosters[user]

        # Step 3: choose the best starter at each position from the full roster
        starters = []

        for position in required_positions:
            players_at_position = []

            for player in user_roster:
                if player["position"] == position:
                    players_at_position.append(player)

            best_player = max(
                players_at_position,
                key=lambda player: player["overall"]
            )

            starters.append(best_player)

        # Step 4: everyone not selected as a starter becomes bench
        bench = []

        for player in user_roster:
            if player not in starters:
                bench.append(player)

        bench.sort(
            key=lambda player: player["overall"],
            reverse=True
        )

        rosters[user] = {
            "starters": starters,
            "bench": bench
        }

    return rosters
