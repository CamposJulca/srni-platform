import { useState } from "react";
import "../assets/dashboard.css";

export default function AppLayout({
  title,
  username,
  onLogout,

  onGoHome,
  onGoDashboard,
  onGoSql,
  onGoNLQuery,
  onGoColaboradores,
  onGoAutomatizacion,
  onGoSinapsis,

  children,
}) {
  const [openConsultas, setOpenConsultas] = useState(false);

  return (
    <div className="dashboard-body">
      <header className="dashboard-header">
        <div className="dashboard-topbar">
          {/* IZQUIERDA */}
          <div className="header-left">
            <div className="header-logo-wrap">
              <img
                src="/logo-unidad-victimas.png"
                alt="Unidad para las Víctimas"
                className="header-logo"
              />
            </div>

            <div className="header-text">
              <h1 className="header-title">{title}</h1>
              <span className="header-hello">Hola, {username}</span>
            </div>
          </div>

          {/* CENTRO: MENU GLOBAL */}
          <nav className="header-menu">
            <button type="button" onClick={() => onGoHome?.()}>
              Inicio
            </button>

            <button type="button" onClick={() => onGoDashboard?.()}>
              Dashboard
            </button>

            {/* Dropdown “Consultas” */}
            <div
              style={{ position: "relative", display: "inline-block" }}
              onMouseLeave={() => setOpenConsultas(false)}
            >
              <button
                type="button"
                onClick={() => setOpenConsultas((v) => !v)}
                aria-expanded={openConsultas}
              >
                Consultas ▾
              </button>

              {openConsultas && (
                <div
                  style={{
                    position: "absolute",
                    top: "42px",
                    left: 0,
                    background: "#fff",
                    border: "1px solid #d7d7d7",
                    borderRadius: "10px",
                    boxShadow: "0 14px 40px rgba(0,0,0,0.18)",
                    padding: "8px",
                    zIndex: 9999,
                    minWidth: "170px",
                  }}
                >
                  <button
                    type="button"
                    style={{
                      width: "100%",
                      textAlign: "left",
                      padding: "10px 12px",
                      borderRadius: "8px",
                      border: "none",
                      background: "transparent",
                      cursor: "pointer",
                    }}
                    onClick={() => {
                      setOpenConsultas(false);
                      onGoSql?.();
                    }}
                  >
                    Query SQL
                  </button>

                  <button
                    type="button"
                    style={{
                      width: "100%",
                      textAlign: "left",
                      padding: "10px 12px",
                      borderRadius: "8px",
                      border: "none",
                      background: "transparent",
                      cursor: "pointer",
                    }}
                    onClick={() => {
                      setOpenConsultas(false);
                      onGoNLQuery?.();
                    }}
                  >
                    NLQuery
                  </button>
                </div>
              )}
            </div>

            <button type="button" onClick={() => onGoColaboradores?.()}>
              Colaboradores
            </button>

            <button type="button" onClick={() => onGoAutomatizacion?.()}>
              Automatización
            </button>

            <button type="button" onClick={() => onGoSinapsis?.()}>
              Sinapsis
            </button>
          </nav>

          {/* DERECHA */}
          <div className="header-right">
            <button className="btn-logout" type="button" onClick={() => onLogout?.()}>
              Cerrar sesión
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-container">{children}</main>
    </div>
  );
}
