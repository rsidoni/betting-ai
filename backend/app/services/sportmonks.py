import requests
from datetime import datetime, timezone
from functools import lru_cache

from app.config import SPORTMONKS_API_KEY, BASE_URL


def _parse_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    except Exception:
        return None


@lru_cache(maxsize=1)
def fetch_upcoming_fixtures():

    url = f"{BASE_URL}/fixtures"

    params = {
        "api_token": SPORTMONKS_API_KEY,
        "include": "league;participants",
        "per_page": 50
    }

    try:
        response = requests.get(url, params=params, timeout=20)

        if response.status_code != 200:
            print("SportMonks Error:", response.status_code, response.text)
            return []

        data = response.json().get("data", [])

        now = datetime.now(timezone.utc)

        future_matches = []

        for match in data:

            start = _parse_date(match.get("starting_at"))

            # se non riesce a leggere la data → lo scarta
            if start is None:
                continue

            # solo match futuri
            if start >= now:
                future_matches.append(match)

        # ordinamento per data
        future_matches.sort(key=lambda x: x.get("starting_at", ""))

        return future_matches

    except Exception as e:
        print("SportMonks Exception:", e)
        return []