from datetime import datetime

def calculate_strength(team_name: str):
    """
    Engine base V11 → simulazione forza squadra
    (in futuro lo colleghiamo a stats reali)
    """

    name = team_name.lower()

    # ranking fittizio stabile (base AI semplice)
    base = 50

    if "celtic" in name or "rangers" in name:
        base += 20
    if "københavn" in name or "copenhagen" in name:
        base += 18
    if "hibernian" in name:
        base += 5
    if "motherwell" in name:
        base += 2
    if "dunfermline" in name:
        base -= 5
    if "partick" in name:
        base -= 3

    return base


def predict_match(match: dict):
    """
    INPUT: fixture SportMonks
    OUTPUT: match con predictions
    """

    try:
        teams = match["name"].split(" vs ")

        home = teams[0]
        away = teams[1]

        home_strength = calculate_strength(home)
        away_strength = calculate_strength(away)

        total = home_strength + away_strength

        home_win = round((home_strength / total) * 100, 2)
        away_win = round((away_strength / total) * 100, 2)

        draw = round(100 - (home_win + away_win), 2)

        confidence = round(abs(home_strength - away_strength), 2)

        match["prediction"] = {
            "home_win": home_win,
            "draw": draw,
            "away_win": away_win,
            "confidence": confidence
        }

        return match

    except Exception as e:
        print("❌ Prediction error:", e)
        return match