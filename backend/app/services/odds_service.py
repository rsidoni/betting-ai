import requests
from app.config import ODDS_API_KEY


def fetch_odds():

    try:
        url = "https://api.the-odds-api.com/v4/sports/soccer/odds"

        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "eu",
            "markets": "h2h,totals",
            "oddsFormat": "decimal"
        }

        r = requests.get(url, params=params, timeout=20)

        if r.status_code != 200:
            return []

        return r.json()

    except Exception as e:
        print("Odds API error:", e)
        return []