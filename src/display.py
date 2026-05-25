def calculate_average_overall(roster: list[dict]) -> float:
    """
    Calculates the average overall rating of a roster.
    """
    total_overall = 0

    for player in roster:
        total_overall += player["overall"]

    return total_overall / len(roster)


def display_player(player: dict) -> None:
    """
    Displays one player.
    """
    print(
        f"{player['position']} - {player['name']} | "
        f"{player['team']} | {player['overall']} OVR"
    )


def display_rosters(rosters: dict[str, dict[str, list[dict]]]) -> None:
    """
    Displays each user's roster with starters and bench separated.
    """
    print("\nGenerated NBA 2K Rosters")
    print("=" * 40)

    for user, roster_sections in rosters.items():
        starters = roster_sections["starters"]
        bench = roster_sections["bench"]
        full_roster = starters + bench

        average_overall = calculate_average_overall(full_roster)

        print(f"\n{user}'s Team")
        print(f"Average Overall: {average_overall:.1f}")
        print("-" * 30)

        print("Starters")
        for player in starters:
            display_player(player)

        if bench:
            print("\nBench")
            for player in bench:
                display_player(player)