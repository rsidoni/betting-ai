import random

# =========================
# STEP 3 PRO ENGINE
# =========================

def get_team_form(match):
    return random.randint(1, 5)


def get_goal_strength(match):
    return random.uniform(0.8, 1.2)


def calculate_prediction(match):

    home = 40
    away = 40
    draw = 20

    # =========================
    # TEAM FORM
    # =========================
    home_form = get_team_form(match)
    away_form = get_team_form(match)

    home += home_form * 2
    away += away_form * 2

    # =========================
    # GOAL STRENGTH
    # =========================
    home *= get_goal_strength(match)
    away *= get_goal_strength(match)

    # =========================
    # HOME ADVANTAGE
    # =========================
    home += 6

    # =========================
    # MATCH STATE IMPACT
    # =========================
    if match.get("state_id") == 1:
        home += 3

    elif match.get("state_id") == 5:
        away += 3

    # =========================
    # NORMALIZATION
    # =========================
    total = home + away + draw

    home_pct = round((home / total) * 100, 2)
    away_pct = round((away / total) * 100, 2)
    draw_pct = round((draw / total) * 100, 2)

    confidence = min(
        60,
        abs(home_pct - away_pct)
    )

    # ✅ TEST ENGINE ATTIVO
    print("🔥 V3 PRO ENGINE ACTIVE")

    return {
        "home_win": home_pct,
        "away_win": away_pct,
        "draw": draw_pct,
        "confidence": round(confidence, 2)
    }