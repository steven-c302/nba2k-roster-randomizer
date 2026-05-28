from flask import Flask, render_template, request
from src.data_loader import load_players
from src.filters import filter_players_by_overall
from src.randomizer import create_rosters_with_starters

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    # Parse form inputs
    names_input = request.form.get("users", "")
    users = [name.strip() for name in names_input.split(",") if name.strip()]

    errors = []

    if not users:
        errors.append("Please enter at least one user name.")

    try:
        team_size = int(request.form.get("team_size", 0))
        if not (5 <= team_size <= 15):
            errors.append("Team size must be between 5 and 15.")
    except ValueError:
        errors.append("Team size must be a number between 5 and 15.")
        team_size = 0

    try:
        min_overall = int(request.form.get("min_overall", 0))
        max_overall = int(request.form.get("max_overall", 0))
        if min_overall > max_overall:
            errors.append("Minimum overall must be less than or equal to maximum overall.")
    except ValueError:
        errors.append("Overall ratings must be numbers.")
        min_overall = 0
        max_overall = 0

    if errors:
        return render_template("index.html", errors=errors)

    players = load_players("data/players.json")
    filtered_players = filter_players_by_overall(players, min_overall, max_overall)
    rosters = create_rosters_with_starters(users, filtered_players, team_size)

    if rosters is None:
        errors.append("Not enough players match your filters. Try widening your overall range or reducing team size.")
        return render_template("index.html", errors=errors)

    # Calculate average OVR per team for display
    averages = {}
    for user, sections in rosters.items():
        full_roster = sections["starters"] + sections["bench"]
        total = sum(p["overall"] for p in full_roster)
        averages[user] = round(total / len(full_roster), 1)

    return render_template("results.html", rosters=rosters, averages=averages)


if __name__ == "__main__":
    app.run(debug=True)
