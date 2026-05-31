from datetime import datetime


def process_fixtures(fixtures: list):
    """
    ENGINE PULIZIA MATCH:
    - normalizza struttura
    - filtra match invalidi
    - rimuove dati rotti API
    """

    cleaned = []

    for f in fixtures:

        try:
            name = f.get("name") or f.get("label")

            if not name:
                continue

            cleaned.append({
                "id": f.get("id"),
                "name": name,
                "home": f.get("home"),
                "away": f.get("away"),
                "league": f.get("league"),
                "starting_at": f.get("starting_at"),
            })

        except Exception as e:
            print("Fixture engine error:", e)
            continue

    # opzionale: ordinamento per data
    try:
        cleaned.sort(key=lambda x: x.get("starting_at") or "")
    except:
        pass

    return cleaned