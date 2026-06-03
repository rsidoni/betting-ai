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

        print("\n===== SPORTMONKS REQUEST =====")
        print("URL:", url)
        print("PARAMS:", params)

        r = requests.get(url, params=params, timeout=20)

        print("SPORTMONKS STATUS:", r.status_code)

        if r.status_code != 200:
            print("SPORTMONKS ERROR RESPONSE:")
            print(r.text[:1000])
            return []

        data = r.json().get("data", [])

        print("SPORTMONKS FIXTURES FOUND:", len(data))

        return data

    except Exception as e:
        print("SPORTMONKS EXCEPTION:", str(e))
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

        print("\n===== FOOTBALL-DATA REQUEST =====")
        print("URL:", url)

        r = requests.get(url, headers=headers, timeout=20)

        print("FOOTBALL-DATA STATUS:", r.status_code)

        if r.status_code != 200:
            print("FOOTBALL-DATA ERROR RESPONSE:")
            print(r.text[:1000])
            return []

        data = r.json().get("matches", [])

        print("FOOTBALL-DATA MATCHES FOUND:", len(data))

        normalized = []

        for m in data:
            normalized.append({
                "id": m.get("id"),
                "name": f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}",
                "starting_at": m.get("utcDate"),
                "home": m["homeTeam"]["name"],
                "away": m["awayTeam"]["name"],
                "league": m.get("competition", {}).get("name")
            })

        return normalized

    except Exception as e:
        print("FOOTBALL-DATA EXCEPTION:", str(e))
        return []


# =========================
# MASTER FIXTURES PIPELINE
# =========================
def fetch_upcoming_fixtures():

    print("\n==============================")
    print("START FETCH FIXTURES")
    print("==============================")

    sm = fetch_sportmonks_fixtures()

    print("SPORTMONKS RETURNED:", len(sm))

    if sm:
        print("USING SPORTMONKS DATA")
        return sm

    print("SPORTMONKS EMPTY -> TRY FOOTBALL-DATA")

    fb = fetch_football_data_fixtures()

    print("FOOTBALL-DATA RETURNED:", len(fb))

    if fb:
        print("USING FOOTBALL-DATA DATA")
        return fb

    print("NO FIXTURES FROM ANY PROVIDER")

    return []
