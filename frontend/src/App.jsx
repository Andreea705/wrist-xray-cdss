import { useState } from "react";
import Login from "./Login";
import Home from "./Home";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  function handleLogin(t) {
    localStorage.setItem("token", t);
    setToken(t);
  }

  function handleLogout() {
    localStorage.removeItem("token");
    setToken(null);
  }

  return token ? (
    <Home token={token} onLogout={handleLogout} />
  ) : (
    <Login onLogin={handleLogin} />
  );
}