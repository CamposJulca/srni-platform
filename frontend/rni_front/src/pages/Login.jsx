import { useState } from "react";
import { login } from "../api/auth";
import "../assets/login.css";

export default function Login({ onLoggedIn }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);

    try {
      await login(username, password);
      onLoggedIn?.(); // avisa al App que ya hay sesión
    } catch (err) {
      setError(err?.message || "Usuario o contraseña incorrectos");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-wrapper">
      <div className="login-card">
        {/* ⬇️ public/ se usa por URL directa */}
<div className="login-logo-wrap">
  <img
    src="/logo-unidad-victimas.png"
    alt="Unidad para las Víctimas"
    className="login-logo"
  />
</div>

        <h2>Bienvenido a RNI</h2>
        <p className="subtitle">Ingreso institucional</p>

        {error ? <div className="error">{error}</div> : null}

        <form onSubmit={handleSubmit} id="login-form">
          <div className="field">
            <label htmlFor="id_username">Correo institucional</label>
            <input
              id="id_username"
              type="text"
              placeholder="usuario@unidadvictimas.gov.co"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoComplete="username"
            />
          </div>

          <div className="field">
            <label htmlFor="id_password">Contraseña</label>
            <input
              id="id_password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </div>

          <button type="submit" className="btn-primary" disabled={busy}>
            {busy ? "Ingresando..." : "Iniciar sesión"}
          </button>
        </form>
      </div>
    </div>
  );
}
