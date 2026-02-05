import { useState } from "react";
import "../assets/login.css";
import { login } from "../api/auth";

export default function Login({ onLoginOk }) {
  const [username, setUsername] = useState("usuario@unidadvictimas.gov.co");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await login(username, password);
      onLoginOk?.();
    } catch (err) {
      setError(err.message || "No se pudo iniciar sesión");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-wrapper">
      <div className="login-card">
        <div className="login-logo-wrap">
          <img
            className="login-logo"
            src="/logo-unidad-victimas.png"
            alt="Unidad para las Víctimas"
          />
        </div>

        <h2>Bienvenido a RNI</h2>
        <p className="subtitle">Ingreso institucional</p>

        {error && (
          <div className="error">
            <b>Error:</b> {error}
          </div>
        )}

        <form onSubmit={submit}>
          <div className="field">
            <label>Correo institucional</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
            />
          </div>

          <div className="field">
            <label>Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>

          <button className="btn-primary" type="submit" disabled={busy}>
            {busy ? "Ingresando..." : "Iniciar sesión"}
          </button>
        </form>
      </div>
    </div>
  );
}
