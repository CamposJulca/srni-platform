import { useEffect, useState } from "react";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Colaboradores from "./pages/Colaboradores";
import Automatizacion from "./pages/Automatizacion";
import PosicionarFirma from "./pages/PosicionarFirma";
import { me } from "./api/auth";

export default function App() {
  const [loading, setLoading] = useState(true);
  const [isAuth, setIsAuth] = useState(false);

  // router por estado
  const [screen, setScreen] = useState("home");
  // home | dashboard | colaboradores | automatizacion | posicionarFirma | sql

  useEffect(() => {
    (async () => {
      try {
        const data = await me();
        const ok = !!data?.authenticated;
        setIsAuth(ok);
        if (ok) setScreen("home");
      } catch {
        setIsAuth(false);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return null;

  // NO AUTH → LOGIN
  if (!isAuth) {
    return (
      <Login
        onLoggedIn={() => {
          setIsAuth(true);
          setScreen("home");
        }}
      />
    );
  }

  // NAV GLOBAL (lo pasamos a todas las pantallas)
  const nav = {
    onGoHome: () => setScreen("home"),
    onGoDashboard: () => setScreen("dashboard"),
    onGoSql: () => alert("Pendiente: módulo Query SQL"),
    onGoColaboradores: () => setScreen("colaboradores"),
    onGoAutomatizacion: () => setScreen("automatizacion"),
  };

  const onAppLogout = () => {
    setIsAuth(false);
    setScreen("home");
  };

  // HOME
  if (screen === "home") {
    return <Home {...nav} onLogoutApp={onAppLogout} />;
  }

  // DASHBOARD
  if (screen === "dashboard") {
    return <Dashboard {...nav} onLogout={onAppLogout} />;
  }

  // COLABORADORES
  if (screen === "colaboradores") {
    return <Colaboradores {...nav} onLogout={onAppLogout} />;
  }

  // AUTOMATIZACIÓN
  if (screen === "automatizacion") {
    return (
      <Automatizacion
        {...nav}
        onLogout={onAppLogout}
        onGoPosicionarFirma={() => setScreen("posicionarFirma")}
      />
    );
  }

  // POSICIONAR FIRMA
  if (screen === "posicionarFirma") {
    return (
      <PosicionarFirma
        {...nav}
        onLogout={onAppLogout}
        onDone={() => setScreen("automatizacion")}
      />
    );
  }

  // fallback
  return <Home {...nav} onLogoutApp={onAppLogout} />;
}
