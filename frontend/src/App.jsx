import { useEffect, useState } from "react";
import axios from "axios";

function App() {

  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  // 🔥 AUTO-DETECT: PC o TELEFONO
  const API_BASE =
    window.location.hostname === "localhost"
      ? "http://127.0.0.1:8000"
      : "http://192.168.1.8:8000";

  useEffect(() => {

    axios
      .get(`${API_BASE}/predictions`)
      .then((res) => {

        console.log("API RESPONSE:", res.data);

        setMatches(res.data.data || []);
        setLoading(false);

      })
      .catch((err) => {

        console.error("API ERROR:", err);

        setError(true);
        setLoading(false);

      });

  }, []);

  if (loading) return <h2>Loading...</h2>;

  if (error) return <h2>Errore caricamento partite</h2>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>

      <h1>⚽ Betting AI</h1>

      {matches.length === 0 && (
        <p>Nessuna partita trovata</p>
      )}

      {matches.map((match) => {

        const markets = match.markets;

        return (
          <div
            key={match.id}
            style={{
              border: "1px solid #ddd",
              borderRadius: "10px",
              padding: "15px",
              marginBottom: "15px"
            }}
          >

            {/* MATCH INFO */}
            <h3>{match.name}</h3>

            <p>📅 {match.starting_at}</p>

            <p>🏁 {match.result_info || "Match non concluso"}</p>

            {/* PREDICTION */}
            <p>
              Home: {match.prediction.home_win}% |{" "}
              Away: {match.prediction.away_win}% |{" "}
              Draw: {match.prediction.draw}%
            </p>

            {/* MARKETS */}
            {markets && (
              <div
                style={{
                  marginTop: "10px",
                  padding: "10px",
                  background: "#f5f5f5",
                  borderRadius: "8px"
                }}
              >

                <h4>📊 Markets</h4>

                <p>
                  1X2 → H {markets["1x2"].home}% |{" "}
                  D {markets["1x2"].draw}% |{" "}
                  A {markets["1x2"].away}%
                </p>

                <p>
                  Over 2.5 → YES {markets.over_2_5.yes}% |{" "}
                  NO {markets.over_2_5.no}%
                </p>

                <p>
                  BTTS → YES {markets.btts.yes}% |{" "}
                  NO {markets.btts.no}%
                </p>

              </div>
            )}

          </div>
        );

      })}

    </div>
  );
}

export default App;