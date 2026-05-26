import random

def calculate_prediction(match):

    # =========================
    # BASE DATA
    # =========================
    home = match.get("home_team", {}).get("name", "Home")
    away = match.get("away_team", {}).get("name", "Away")

    home_id = match.get("home_team", {}).get("id", 1)
    away_id = match.get("away_team", {}).get("id", 2)

    # =========================
    # STEP 3 AI (REALISTIC ENGINE V1)
    # =========================

    # fake but stable “team strength” baseline
    home_strength = (home_id % 10) + random.uniform(0, 5)
    away_strength = (away_id % 10) + random.uniform(0, 5)

    # home advantage
    home_strength += 2.0

    # expected goals model (simple Poisson-like proxy)
    home_goals = (home_strength / (away_strength + 1)) * 1.5
    away_goals = (away_strength / (home_strength + 1)) * 1.2

    # probabilities (normalized soft model)
    total = home_goals + away_goals + 2.5

    home_win = (home_goals / total) * 100
    away_win = (away_goals / total) * 100
    draw = (2.5 / total) * 100

    # confidence model
    confidence = abs(home_goals - away_goals) * 10

    return {
        "home_win": round(home_win, 2),
        "away_win": round(away_win, 2),
        "draw": round(draw, 2),
        "confidence": round(confidence, 2)
    }