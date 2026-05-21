def calculate_average_overall(roster: list[dict]) -> float:
    """
    Calculates the average overall rating of a roster.
    """
    total_overall = 0

    for player in roster:
        total_overall += player["overall"]

    return total_overall / len(roster)


def display_rosters(rosters: dict[str, list[dict]]) -> None:
    """
    Displays generated rosters in the terminal.
    """
    print("\nGenerated NBA 2K Rosters")
    print("=" * 40)

    for user, roster in rosters.items():
        average_overall = calculate_average_overall(roster)

        print(f"\n{user}'s Team")
        print(f"Average Overall: {average_overall:.1f}")
        print("-" * 30)

        for player in roster:
            print(
                f"{player['name']} | {player['position']} | "
                f"{player['team']} | {player['overall']} OVR"
            )