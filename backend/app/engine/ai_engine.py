import math


def poisson_probability(lmbda, k):
    return (lmbda ** k * math.exp(-lmbda)) / math.factorial(k)


def expected_goals(team_strength, opponent_strength):
    return round((team_strength * 0.7 + opponent_strength * 0.3), 2)


def normalize_three_way(home, draw, away):
    total = home + draw + away

    if total <= 0:
        return 33.33, 33.33, 33.33

    return (
        round(home / total * 100, 2),
        round(draw / total * 100, 2),
        round(away / total * 100, 2),
    )


def normalize_two_way(a, b):
    total = a + b

    if total <= 0:
        return 50.0, 50.0

    return (
        round(a / total * 100, 2),
        round(b / total * 100, 2),
    )


def generate_prediction(home_strength, away_strength):

    home_xg = expected_goals(home_strength, away_strength)
    away_xg = expected_goals(away_strength, home_strength)

    home_raw = poisson_probability(home_xg, 2) * 100
    away_raw = poisson_probability(away_xg, 1) * 100

    draw_raw = max(0, 100 - (home_raw + away_raw))

    home, draw, away = normalize_three_way(home_raw, draw_raw, away_raw)

    over_yes_raw = (home_xg + away_xg) * 25
    over_no_raw = draw * 0.5

    over_yes, over_no = normalize_two_way(over_yes_raw, over_no_raw)

    return {
        "home": home,
        "draw": draw,
        "away": away,
        "home_xg": home_xg,
        "away_xg": away_xg,
        "over_2_5": {
            "yes": over_yes,
            "no": over_no
        }
    }