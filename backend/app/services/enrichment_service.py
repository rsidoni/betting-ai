from app.services.odds_service import fetch_odds


def enrich_with_odds(matches):

    odds_data = fetch_odds()

    if not odds_data:
        return matches

    enriched = []

    for m in matches:

        m_name = m.get("name", "").lower()

        match_odds = None

        for o in odds_data:
            if o.get("home_team", "").lower() in m_name:
                match_odds = o
                break

        if match_odds:
            m["odds"] = match_odds.get("bookmakers", [])

        enriched.append(m)

    return enriched