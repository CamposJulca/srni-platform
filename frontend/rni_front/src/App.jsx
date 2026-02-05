import { useEffect, useState } from "react";
import { me } from "./api/auth";

import Login from "./pages/Login";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Colaboradores from "./pages/Colaboradores";
import Automatizacion from "./pages/Automatizacion";
import QuerySQL from "./pages/QuerySQL";
import NLQuery from "./pages/NLQuery";
import Sinapsis from "./pages/Sinapsis";

export default function App() {
  // ✅ Nunca dejamos pantalla en blanco: por defecto login.
  const [view, setView] = useState("login");

  useEffect(() => {
    let alive = true;

    (async () => {
      try {
        await me(); // usa tu auth.js tal cual
        if (alive) setView("home");
      } catch {
        if (alive) setView("login");
      }
    })();

    return () => {
      alive = false;
    };
  }, []);

  function go(v) {
    setView(v);
  }

  function handleLogoutApp() {
    setView("login");
  }

  const nav = {
    onGoHome: () => go("home"),
    onGoDashboard: () => go("dashboard"),
    onGoSql: () => go("sql"),
    onGoNLQuery: () => go("nlquery"),
    onGoColaboradores: () => go("colaboradores"),
    onGoAutomatizacion: () => go("automatizacion"),
    onGoSinapsis: () => go("sinapsis"),
  };

  if (view === "login") {
    return <Login onLoginOk={() => go("home")} />;
  }

  if (view === "home") return <Home {...nav} onLogoutApp={handleLogoutApp} />;
  if (view === "dashboard") return <Dashboard {...nav} onLogout={handleLogoutApp} />;
  if (view === "sql") return <QuerySQL {...nav} onLogout={handleLogoutApp} />;
  if (view === "nlquery") return <NLQuery {...nav} onLogout={handleLogoutApp} />;
  if (view === "colaboradores") return <Colaboradores {...nav} onLogout={handleLogoutApp} />;
  if (view === "automatizacion") return <Automatizacion {...nav} onLogout={handleLogoutApp} />;
  if (view === "sinapsis") return <Sinapsis {...nav} onLogout={handleLogoutApp} />;

  return <Login onLoginOk={() => go("home")} />;
}
