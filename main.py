from src.data_loader import load_players
from src.filters import filter_players_by_overall
from src.randomizer import create_rosters_with_starters
from src.display import display_rosters



def get_user_names() -> list[str]:
    """Asks for the users/friends who need generated teams."""
    names_input = input("Enter user names separated by commas: ")

    users = []

    for name in names_input.split(","):
        cleaned_name = name.strip()

        if cleaned_name:
            users.append(cleaned_name)

    return users


def get_team_size() -> int:
    """Asks how many NBA players should be on each user's team. Team size should be between 5 - 15."""
    while True:
        try:
            team_size = int(input("Enter team size (5-15): "))

            if 5 <= team_size <= 15:
                return team_size
            else:
                print("Team size must be between 5 and 15. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 5 and 15.")
            


def get_overall_filter() -> tuple[int, int]:
    """Asks for the minimum and maximum overall rating."""
    while True:
        try:
            min_overall = int(input("Enter minimum player overall: "))
            max_overall = int(input("Enter maximum player overall: "))

            if min_overall > max_overall:
                print("Minimum overall must be less than or equal to maximum. Please try again.")
            else:
                return min_overall, max_overall
        except ValueError:
            print("Invalid input. Please enter a number.")


def main() -> None:
    players = load_players("data/players.json")

    users = get_user_names()
    team_size = get_team_size()
    min_overall, max_overall = get_overall_filter()

    filtered_players = filter_players_by_overall(
        players,
        min_overall,
        max_overall
    )

    rosters = create_rosters_with_starters(
        users,
        filtered_players,
        team_size
    )

    if rosters is None:
        print("Not enough players match your filters.")
        return

    display_rosters(rosters)


if __name__ == "__main__":
    main()