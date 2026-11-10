import { useEffect, useState } from "react";
import "./Home.css";

const API = "http://localhost:8000";
const STATUS = { waiting: "Wartet", imaged: "Geröntgt", reported: "Befundet" };

export default function Home({ token, onLogout }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/dashboard`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => {
        if (r.status === 401) {
          onLogout(); // Token abgelaufen oder ungültig
          return null;
        }
        return r.json();
      })
      .then((d) => d && setData(d))
      .catch(() => setError("Server nicht erreichbar"));
  }, [token, onLogout]);

  if (error) return <p className="dash-error">{error}</p>;
  if (!data) return <p className="dash-loading">Lädt …</p>;

  const { stats, patients } = data;

  return (
    <div className="dash">
      <header className="dash-header">
        <div>
          <h1>{data.hospital}</h1>
          <p>{data.department} · angemeldet als {data.doctor}</p>
        </div>
        <button onClick={onLogout}>Abmelden</button>
      </header>

      <section className="dash-stats">
        <div className="stat"><span>{stats.total}</span>Patienten heute</div>
        <div className="stat"><span>{stats.waiting}</span>Warten auf Röntgen</div>
        <div className="stat"><span>{stats.imaged}</span>Geröntgt</div>
        <div className="stat"><span>{stats.reported}</span>Befundet</div>
      </section>

      <section>
        <h2>Patientenliste</h2>
        <table className="dash-table">
          <thead>
            <tr>
              <th>ID</th><th>Alter</th><th>Geschlecht</th><th>Seite</th>
              <th>Ankunft</th><th>Beschwerde</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.age} J.</td>
                <td>{p.sex}</td>
                <td>{p.side}</td>
                <td>{p.arrival}</td>
                <td>{p.complaint}</td>
                <td><span className={`badge ${p.status}`}>{STATUS[p.status]}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <button disabled style={{ marginTop: 16 }}>
          Röntgenbild hochladen (bald verfügbar)
        </button>
      </section>
    </div>
  );
}