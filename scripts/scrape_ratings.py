"""
Scrapes NBA 2K26 player ratings from 2kratings.com and writes data/players.json.

Usage:
    python scripts/scrape_ratings.py
"""

import json
import time
import sys
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Run:  pip install requests beautifulsoup4")
    sys.exit(1)


# --- Paste the URL from "See Top 100 Current Players" here ---
RATINGS_URL = "https://www.2kratings.com/lists/top-100-highest-nba-2k-ratings"

OUTPUT_PATH = Path("data/players.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# Abbreviation → full team name
TEAM_NAMES = {
    "ATL": "Atlanta Hawks",
    "BOS": "Boston Celtics",
    "BKN": "Brooklyn Nets",
    "CHA": "Charlotte Hornets",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DAL": "Dallas Mavericks",
    "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons",
    "GSW": "Golden State Warriors",
    "HOU": "Houston Rockets",
    "IND": "Indiana Pacers",
    "LAC": "LA Clippers",
    "LAL": "Los Angeles Lakers",
    "MEM": "Memphis Grizzlies",
    "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks",
    "MIN": "Minnesota Timberwolves",
    "NOP": "New Orleans Pelicans",
    "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder",
    "ORL": "Orlando Magic",
    "PHI": "Philadelphia 76ers",
    "PHX": "Phoenix Suns",
    "POR": "Portland Trail Blazers",
    "SAC": "Sacramento Kings",
    "SAS": "San Antonio Spurs",
    "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz",
    "WAS": "Washington Wizards",
}

VALID_POSITIONS = {"PG", "SG", "SF", "PF", "C"}


def parse_players(soup: BeautifulSoup) -> list[dict]:
    players = []

    # The table uses id="lists-table" on this page
    table = soup.find("table", id="lists-table")
    if not table:
        print("ERROR: Could not find #lists-table. The page structure may have changed.")
        return players

    tbody = table.find("tbody")
    if not tbody:
        print("ERROR: Could not find table body.")
        return players

    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        player_cell = cells[1]

        # --- Player name ---
        # Sits in <a class="player-name">
        name_tag = player_cell.find("a", class_="player-name")
        if not name_tag:
            continue
        name = name_tag.get_text(strip=True)

        # --- Position and team ---
        # Both live inside <span class="entry-subtext-font ...">
        # Structure: <a href="/lists/center">C</a> | <a href="/lists/6-11-height">6'11"</a> | <a href="/teams/denver-nuggets">DEN</a>
        subtext = player_cell.find("span", class_=lambda c: c and "entry-subtext-font" in c.split())
        if not subtext:
            continue

        position = None
        team_abbr = None

        for link in subtext.find_all("a"):
            href = link.get("href", "")
            text = link.get_text(strip=True).upper()

            if "/teams/" in href:
                team_abbr = text                        # e.g. "DEN"
            elif "/lists/" in href and "height" not in href:
                if text in VALID_POSITIONS:
                    position = text                     # e.g. "C"

        if not position or not team_abbr:
            continue

        team = TEAM_NAMES.get(team_abbr, team_abbr)

        # --- Overall rating ---
        # Third cell contains <span class="attribute-box ...">98</span>
        ovr_span = cells[2].find("span", class_="attribute-box")
        if not ovr_span:
            continue
        try:
            overall = int(ovr_span.get_text(strip=True))
        except ValueError:
            continue

        players.append({
            "name":     name,
            "team":     team,
            "position": position,
            "overall":  overall,
        })

    return players


def scrape(url: str) -> list[dict]:
    print(f"Fetching {url} ...")
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    players = parse_players(soup)

    print(f"Parsed {len(players)} players from page.")
    return players


def main() -> None:
    if RATINGS_URL == "PASTE_URL_HERE":
        print("Open scripts/scrape_ratings.py and set RATINGS_URL to the Top 100 players page URL.")
        sys.exit(1)

    players = scrape(RATINGS_URL)

    if not players:
        print("No players scraped. Run with --debug to see raw HTML.")
        sys.exit(1)

    players.sort(key=lambda p: p["overall"], reverse=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=2)

    print(f"Wrote {len(players)} players → {OUTPUT_PATH}")


if __name__ == "__main__":
    if "--debug" in sys.argv:
        # Dump raw HTML so you can inspect the structure manually
        r = requests.get(RATINGS_URL, headers=HEADERS, timeout=15)
        Path("data/debug.html").write_text(r.text, encoding="utf-8")
        print("Raw HTML saved to data/debug.html")
        sys.exit(0)

    main()
