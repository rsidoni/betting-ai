import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.get(`${API_BASE}/matches`, {
        timeout: 15000,
      });

      if (response.data?.matches) {
        setMatches(response.data.matches);
      } else {
        setMatches([]);
      }
    } catch (err) {
      console.error(err);
      setError("Errore caricamento partite");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Betting AI</h1>

      {loading && <p>Caricamento...</p>}

      {error && (
        <div
          style={{
            background: "#ffebee",
            padding: 10,
            marginBottom: 20,
            borderRadius: 8,
            color: "red",
          }}
        >
          {error}
        </div>
      )}

      {!loading && matches.length === 0 && (
        <p>Nessuna partita trovata</p>
      )}

      {matches.map((match) => (
        <div
          key={match.id}
          style={{
            border: "1px solid #ccc",
            padding: 15,
            marginBottom: 15,
            borderRadius: 10,
          }}
        >
          <h3>
            {match.home_team} vs {match.away_team}
          </h3>

          <p>
            <strong>League:</strong> {match.league}
          </p>

          <p>
            <strong>Date:</strong> {match.date}
          </p>

          <hr />

          <p>
            <strong>Pronostico 1X2</strong>
          </p>

          <ul>
            <li>Home: {match.prediction?.home}%</li>
            <li>Draw: {match.prediction?.draw}%</li>
            <li>Away: {match.prediction?.away}%</li>
          </ul>

          <p>
            <strong>xG</strong><br />
            Home: {match.prediction?.home_xg}<br />
            Away: {match.prediction?.away_xg}
          </p>

          <p>
            <strong>Over 2.5</strong><br />
            Yes: {match.prediction?.over_2_5?.yes}%<br />
            No: {match.prediction?.over_2_5?.no}%
          </p>
        </div>
      ))}
    </div>
  );
}

export default App;