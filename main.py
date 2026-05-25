from src.data_loader import load_players
from src.filters import filter_players_by_overall, filter_players_by_position
from src.randomizer import create_random_rosters
from src.display import display_rosters



def get_user_names() -> list[str]:
    """
    Asks for the users/friends who need generated teams.
    """
    names_input = input("Enter user names separated by commas: ")

    users = []

    for name in names_input.split(","):
        cleaned_name = name.strip()

        if cleaned_name:
            users.append(cleaned_name)

    return users


def get_team_size() -> int:
    """
    Asks how many NBA players should be on each user's team.
    """
    return int(input("How many NBA players per team? "))


def get_overall_filter() -> tuple[int, int]:
    """Asks for the minimum and maximum overall rating."""
    min_overall = int(input("Enter minimum player overall: "))
    max_overall = int(input("Enter maximum player overall: "))

    return min_overall, max_overall


def main() -> None:
    players = load_players("data/players.json")

    users = get_user_names()
    team_size = get_team_size()
    min_overall, max_overall = get_overall_filter()
    positions = ["PG", "SG", "SF", "PF", "C"]

    filtered_players = filter_players_by_overall(
        players,
        min_overall,
        max_overall
    )

    filtered_players = filter_players_by_position(
        filtered_players,
        positions
    )
    

    rosters = create_random_rosters(
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