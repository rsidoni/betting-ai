import requests
from datetime import datetime, timedelta

from app.config import SPORTMONKS_API_KEY, FOOTBALL_DATA_API_KEY


# =========================
# SPORTMONKS
# =========================
def fetch_sportmonks_fixtures():
    try:
        today = datetime.utcnow().date()
        end = today + timedelta(days=7)

        url = "https://api.sportmonks.com/v3/football/fixtures"

        params = {
            "api_token": SPORTMONKS_API_KEY,
            "include": "league;participants",
            "filters": f"between:{today},{end}",
            "per_page": 50
        }

        r = requests.get(url, params=params, timeout=20)

        if r.status_code != 200:
            return []

        return r.json().get("data", [])

    except Exception as e:
        print("SportMonks error:", e)
        return []


# =========================
# FOOTBALL-DATA (BACKUP)
# =========================
def fetch_football_data_fixtures():
    try:
        url = "https://api.football-data.org/v4/matches"

        headers = {
            "X-Auth-Token": FOOTBALL_DATA_API_KEY
        }

        r = requests.get(url, headers=headers, timeout=20)

        if r.status_code != 200:
            return []

        data = r.json().get("matches", [])

        # normalize structure
        normalized = []
        for m in data:
            normalized.append({
                "id": m.get("id"),
                "name": f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}",
                "starting_at": m.get("utcDate"),
                "home": m['homeTeam']['name'],
                "away": m['awayTeam']['name'],
                "league": m.get("competition", {}).get("name")
            })

        return normalized

    except Exception as e:
        print("Football-data error:", e)
        return []


# =========================
# MASTER FIXTURES PIPELINE
# =========================
def fetch_upcoming_fixtures():

    sm = fetch_sportmonks_fixtures()
    if sm:
        return sm

    fb = fetch_football_data_fixtures()
    if fb:
        return fb

    return []