import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/api/auth/csrf/`, { credentials: "include" }).catch(() => {});
  }, []);

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      // 1) Fuerza cookie CSRF
      await fetch(`${API_BASE}/api/auth/csrf/`, { credentials: "include" });

      const csrfToken = getCookie("csrftoken");
      if (!csrfToken) {
        setError("CSRF no disponible. Revisa /api/auth/csrf/ y cookies.");
        setSubmitting(false);
        return;
      }

      // 2) Login JSON (tu api_login espera JSON)
      const res = await fetch(`${API_BASE}/api/auth/login/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        setError("Usuario o contraseña incorrectos");
        setSubmitting(false);
        return;
      }

      // 3) Redirige al backend (Django) para ver Home/Dashboard real
      window.location.href = `${API_BASE}/dashboard/`;
      // si quieres ir al home Django en vez del dashboard:
      // window.location.href = `${API_BASE}/`;
    } catch {
      setError("Error de red. Revisa backend y cookies.");
      setSubmitting(false);
    }
  }

  return (
    <div className="login-wrapper">
      <div className="login-card">
        <img
          src="/img/logo-unidad-victimas.png"
          alt="Unidad para las Víctimas"
          className="login-logo"
        />

        <h2>Bienvenido a RNI</h2>
        <p className="subtitle">Ingreso institucional</p>

        {error ? <div className="error">{error}</div> : null}

        <form onSubmit={onSubmit} id="login-form">
          <div className="field">
            <label htmlFor="id_username">Correo institucional</label>
            <input
              type="text"
              id="id_username"
              placeholder="usuario@unidadvictimas.gov.co"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
            />
          </div>

          <div className="field">
            <label htmlFor="id_password">Contraseña</label>
            <input
              type="password"
              id="id_password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>

          <button type="submit" className="btn-primary" disabled={submitting}>
            {submitting ? "Ingresando..." : "Iniciar sesión"}
          </button>
        </form>
      </div>
    </div>
  );
}
