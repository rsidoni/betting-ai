from typing import Dict, List


class StatsEngine:

    def calculate_team_strength(self, matches: List[dict], team: str) -> Dict:
        wins = draws = losses = 0

        for m in matches:
            if team in m.get("name", ""):
                if "won" in m.get("result_info", "").lower():
                    wins += 1
                elif "draw" in m.get("result_info", "").lower():
                    draws += 1
                elif "lost" in m.get("result_info", "").lower():
                    losses += 1

        total = max(len(matches), 1)

        return {
            "matches": total,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "win_rate": round(wins / total * 100, 2),
        }


stats_engine = StatsEngine()