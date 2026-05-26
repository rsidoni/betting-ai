import requests
from datetime import datetime, timedelta

SPORTMONKS_KEY = "gXDoV9IT5WDwl7eECjEDjZLSfuYrRlaHeyDzwE6rmXwq5khisVYOaWPnDG8G"


def get_dates():
    today = datetime.utcnow().date()
    return [
        str(today - timedelta(days=1)),
        str(today),
        str(today + timedelta(days=1))
    ]


def fetch_by_date(date_str):
    url = f"https://api.sportmonks.com/v3/football/fixtures/date/{date_str}"

    try:
        r = requests.get(
            url,
            params={"api_token": SPORTMONKS_KEY},
            timeout=10
        )

        data = r.json()

        if "data" not in data:
            return []

        return data["data"]

    except Exception as e:
        print("API ERROR:", e)
        return []