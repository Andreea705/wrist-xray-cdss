import { useState } from "react";
import "./Login.css";

const API = "http://localhost:8000";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        body: new URLSearchParams({ username: username.trim(), password }),
      });
      if (res.status === 401) {
        setError("Benutzername oder Passwort falsch");
        return;
      }
      if (!res.ok) {
        setError(`Serverfehler (${res.status})`);
        return;
      }
      const data = await res.json();
      onLogin(data.access_token);
    } catch {
      setError("Server nicht erreichbar");
    }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleSubmit}>
        <h2>Anmeldung</h2>
        <input
          placeholder="Benutzername"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Passwort"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Anmelden</button>
        {error && <p className="login-error">{error}</p>}
      </form>
    </div>
  );
}