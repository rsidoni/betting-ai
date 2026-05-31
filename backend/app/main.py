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
        m["prediction"] = generate_prediction(
            home_strength=1.2,
            away_strength=1.0
        )

    enriched = enrich_with_odds(clean)

    return {
        "success": True,
        "count": len(enriched),
        "matches": enriched[:50]
    }