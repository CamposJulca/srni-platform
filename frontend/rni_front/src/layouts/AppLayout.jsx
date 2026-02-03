import "../assets/dashboard.css";

export default function AppLayout({
  title,
  username,
  onLogout,

  onGoHome,
  onGoDashboard,
  onGoSql,
  onGoColaboradores,
  onGoAutomatizacion,

  children,
}) {
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
            <button type="button" onClick={() => onGoSql?.()}>
              Query SQL
            </button>
            <button type="button" onClick={() => onGoColaboradores?.()}>
              Colaboradores
            </button>
            <button type="button" onClick={() => onGoAutomatizacion?.()}>
              Automatización
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
