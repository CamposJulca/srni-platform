
import { useEffect, useState } from "react";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import { me } from "./api/auth";

export default function App() {
  const [loading, setLoading] = useState(true);
  const [isAuth, setIsAuth] = useState(false);

  const [screen, setScreen] = useState("home"); // home | dashboard | sql | colaboradores | automatizacion

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

  // NAV GLOBAL
  const nav = {
    onGoHome: () => setScreen("home"),
    onGoDashboard: () => setScreen("dashboard"),
    onGoSql: () => alert("Pendiente: módulo Query SQL"),
    onGoColaboradores: () => alert("Pendiente: módulo Colaboradores"),
    onGoAutomatizacion: () => alert("Pendiente: Automatización Documental"),
  };

  // HOME
  if (screen === "home") {
    return (
      <Home
        {...nav}
        onLogoutApp={() => {
          setIsAuth(false);
          setScreen("home");
        }}
      />
    );
  }

  // DASHBOARD
  if (screen === "dashboard") {
    return (
      <Dashboard
        {...nav}
        onLogout={() => {
          setIsAuth(false);
          setScreen("home");
        }}
      />
    );
  }

  // FALLBACK
  return (
    <Home
      {...nav}
      onLogoutApp={() => {
        setIsAuth(false);
        setScreen("home");
      }}
    />
  );

}
