from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime, timedelta

# 🔥 ENV SUPPORT (SPORTMONKS KEY DA .env)
from dotenv import load_dotenv
import os

load_dotenv()

from app.engine.ai_engine import calculate_prediction

app = FastAPI()

# =========================
# CORS FIX
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CONFIG (DA .env)
# =========================
SPORTMONKS_KEY = os.getenv("SPORTMONKS_KEY")

# =========================
# SAFETY CHECK
# =========================
if not SPORTMONKS_KEY:
    print("❌ ERRORE: SPORTMONKS_KEY NON TROVATA NEL .env")

# =========================
# DATE ENGINE STABILE
# =========================
def get_dates():
    today = datetime.utcnow().date()

    # solo finestre realistiche
    return [
        str(today - timedelta(days=1)),
        str(today)
    ]

# =========================
# FETCH FIXTURES
# =========================
def fetch_fixtures_by_date(date_str: str):

    url = f"https://api.sportmonks.com/v3/football/fixtures/date/{date_str}"

    try:
        r = requests.get(
            url,
            params={"api_token": SPORTMONKS_KEY},
            timeout=20
        )

        data = r.json()

        if "data" not in data:
            print("⚠️ ERROR RESPONSE:", data)
            return []

        return data["data"]

    except Exception as e:
        print("❌ REQUEST ERROR:", str(e))
        return []

# =========================
# MAIN ENDPOINT
# =========================
@app.get("/predictions")
def get_predictions():

    all_matches = []
    seen_ids = set()

    dates = get_dates()

    print("📅 DATES:", dates)

    for d in dates:

        print(f"📅 FETCH {d}")

        matches = fetch_fixtures_by_date(d)

        print("✅ FOUND:", len(matches))

        for m in matches:

            # evita duplicati
            if m["id"] in seen_ids:
                continue

            seen_ids.add(m["id"])

            # prediction AI
            prediction = calculate_prediction(m)
            m["prediction"] = prediction

            # markets engine
            home = prediction["home_win"]
            away = prediction["away_win"]
            draw = prediction["draw"]

            m["markets"] = {
                "1x2": {
                    "home": round(home, 2),
                    "draw": round(draw, 2),
                    "away": round(away, 2),
                },
                "over_2_5": {
                    "yes": round((home + away) * 0.6, 2),
                    "no": round(draw * 0.6, 2),
                },
                "btts": {
                    "yes": round((home + away) * 0.5, 2),
                    "no": round(draw, 2),
                }
            }

            all_matches.append(m)

    return {
        "status": "ok",
        "count": len(all_matches),
        "data": all_matches
    }

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {"status": "backend ok"}