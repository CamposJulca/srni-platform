import AppLayout from "../layouts/AppLayout";
import "../assets/home.css";
import { logout, me } from "../api/auth";
import { useEffect, useState } from "react";

export default function Home({
  onGoHome,
  onGoDashboard,
  onGoSql,
  onGoColaboradores,
  onGoAutomatizacion,
  onLogoutApp,
}) {
  const [username, setUsername] = useState("Usuario");

  useEffect(() => {
    (async () => {
      try {
        const u = await me();
        setUsername(u?.username || "Usuario");
      } catch {
        setUsername("Usuario");
      }
    })();
  }, []);

  async function handleLogout() {
    try {
      await logout();
    } finally {
      onLogoutApp?.();
    }
  }

  return (
    <AppLayout
      title="Inicio – Red Nacional de Información"
      username={username}
      onLogout={handleLogout}
      onGoHome={onGoHome}
      onGoDashboard={onGoDashboard}
      onGoSql={onGoSql}
      onGoColaboradores={onGoColaboradores}
      onGoAutomatizacion={onGoAutomatizacion}
    >
      <div className="home-container">
        <div className="home-header">
          <h1>Bienvenido a la Red Nacional de Información</h1>
          <p>Usuario autenticado correctamente.</p>
        </div>

        <div className="cards-grid">
          <div className="card">
            <h3>Query SQL</h3>
            <p>Consulta controlada de información en PostgreSQL.</p>
            <button className="card-link" onClick={onGoSql}>
              Ingresar
            </button>
          </div>

          <div className="card">
            <h3>Dashboard</h3>
            <p>Indicadores y métricas generales del sistema.</p>
            <button className="card-link" onClick={onGoDashboard}>
              Ver dashboard
            </button>
          </div>

          <div className="card">
            <h3>Colaboradores</h3>
            <p>Gestión y visualización de colaboradores.</p>
            <button className="card-link" onClick={onGoColaboradores}>
              Abrir
            </button>
          </div>

          <div className="card">
            <h3>Automatización Documental</h3>
            <p>Firma masiva de documentos Word, generación de PDFs y descarga en bloque.</p>
            <button className="card-link" onClick={onGoAutomatizacion}>
              Abrir módulo
            </button>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
