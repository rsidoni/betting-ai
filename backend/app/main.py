from fastapi import FastAPI

from app.services.fixtures_service import fetch_upcoming_fixtures
from app.services.enrichment_service import enrich_with_odds
from app.engine.fixture_engine import process_fixtures
from app.engine.ai_engine import generate_prediction

app = FastAPI()


@app.get("/matches")
def get_matches():

    raw = fetch_upcoming_fixtures()

    if not raw:
        return {
            "success": False,
            "message": "No fixtures returned from APIs"
        }

    clean = process_fixtures(raw)

    for m in clean:

        # 🔍 DEBUG INPUT MATCH
        print("\nMATCH INPUT:", m)

        home = m.get("home", "")
        away = m.get("away", "")

        # 🔥 FEATURE SEMPLICE MA DIVERSIFICATA PER MATCH
        # (serve SOLO per debug / miglioramento modello)
        def stable_strength(team_name: str) -> float:
            base = sum(ord(c) for c in team_name.lower())
            return 1.0 + (base % 10) / 10


        home_strength = stable_strength(home)
        away_strength = stable_strength(away)

        features = {
            "home_team": home,
            "away_team": away,
            "home_strength": home_strength,
            "away_strength": away_strength
        }

        # 🔍 DEBUG FEATURE VECTOR
        print("FEATURE VECTOR:", features)

        # 🎯 prediction ora VARIA per match
        m["prediction"] = generate_prediction(
            home_strength=home_strength,
            away_strength=away_strength
        )

    enriched = enrich_with_odds(clean)

    return {
        "success": True,
        "count": len(enriched),
        "matches": enriched[:50]
    }
