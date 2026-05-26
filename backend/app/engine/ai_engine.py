def calculate_prediction(match):

    home = match.get("home_team_id", 1)
    away = match.get("away_team_id", 1)

    # =========================
    # BASE RATINGS (SEED)
    # =========================
    base_home = 50
    base_away = 50
    base_draw = 0

    # =========================
    # HOME ADVANTAGE
    # =========================
    home_advantage = 6

    # =========================
    # FORM SIMULATA (SAFE MODE)
    # =========================
    home_form = (home % 7) + 1
    away_form = (away % 7) + 1

    form_diff = (home_form - away_form) * 2

    # =========================
    # GOAL IMPACT (MODELLO SEMPLICE)
    # =========================
    home_attack = (home % 10) + 1
    away_attack = (away % 10) + 1

    home_defense = (away % 8) + 1
    away_defense = (home % 8) + 1

    goal_factor = (home_attack - away_attack) + (away_defense - home_defense)

    # =========================
    # DRAW FACTOR (REALISTICO)
    # =========================
    draw_bias = 18 - abs(form_diff)

    if draw_bias < 8:
        draw_bias = 8

    # =========================
    # FINAL SCORE MODEL
    # =========================
    home_score = base_home + home_advantage + form_diff + goal_factor
    away_score = base_away - home_advantage - form_diff - goal_factor
    draw_score = draw_bias

    # =========================
    # NORMALIZATION
    # =========================
    total = home_score + away_score + draw_score

    home_win = round((home_score / total) * 100, 2)
    away_win = round((away_score / total) * 100, 2)
    draw = round((draw_score / total) * 100, 2)

    # =========================
    # CONFIDENCE (QUALITY INDEX)
    # =========================
    confidence = round(abs(home_win - away_win), 2)

    # =========================
    # OVER 2.5 (MODEL SIMULATO)
    # =========================
    over_2_5 = round((home_attack + away_attack) * 3, 2)
    if over_2_5 > 80:
        over_2_5 = 80

    # =========================
    # VALUE BET DETECTION
    # =========================
    value_bet = "NONE"

    if home_win > 55:
        value_bet = "HOME"
    elif away_win > 55:
        value_bet = "AWAY"
    elif draw > 40:
        value_bet = "DRAW"

    # =========================
    # RETURN FINAL MODEL
    # =========================
    return {
        "home_win": home_win,
        "away_win": away_win,
        "draw": draw,
        "confidence": confidence,
        "over_2_5": over_2_5,
        "value_bet": value_bet
    }