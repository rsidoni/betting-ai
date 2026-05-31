from fastapi import FastAPI

from app.services.fixtures_service import fetch_upcoming_fixtures
from app.services.enrichment_service import enrich_with_odds
from app.engine.fixture_engine import process_fixtures
from app.engine.ai_engine import generate_prediction


app = FastAPI()


@app.get("/matches")
def get_matches():

    # 1 - FIXTURES (SportMonks + fallback)
    raw = fetch_upcoming_fixtures()

    print("RAW FIXTURES:", len(raw))  # DEBUG

    # 2 - ENGINE CLEAN
    clean = process_fixtures(raw)

    print("CLEAN FIXTURES:", len(clean))  # DEBUG

    # 3 - AI PREDICTIONS
    for m in clean:
        m["prediction"] = generate_prediction(
            home_strength=1.2,
            away_strength=1.0
        )

    # 4 - ODDS ENRICHMENT
    enriched = enrich_with_odds(clean)

    return {
        "success": True,
        "count": len(enriched),
        "matches": enriched[:50]
    }