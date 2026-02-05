// src/App.jsx
import { useEffect, useState } from "react";

import Dashboard from "./pages/Dashboard";
import Colaboradores from "./pages/Colaboradores";
import Automatizacion from "./pages/Automatizacion";
import PosicionarFirma from "./pages/PosicionarFirma";

import QuerySQL from "./pages/QuerySQL";
import NLQuery from "./pages/NLQuery";

import Login from "./pages/Login"; // Si ya tienes Login. Si tu login se llama distinto, cámbialo.

import { me } from "./api/auth";

export default function App() {
  const [page, setPage] = useState("dashboard");

  // Navegación global (mismo patrón de callbacks)
  const nav = {
    onGoHome: () => setPage("dashboard"),
    onGoDashboard: () => setPage("dashboard"),
    onGoSql: () => setPage("sql"),
    onGoNLQuery: () => setPage("nlquery"),
    onGoColaboradores: () => setPage("colaboradores"),
    onGoAutomatizacion: () => setPage("automatizacion"),
    onGoPosicionarFirma: () => setPage("posicionar_firma"),
    onLogout: () => setPage("login"),
  };

  // (Opcional pero recomendado) Si no está autenticado, manda a login
  useEffect(() => {
    (async () => {
      try {
        await me();
        // ok
      } catch {
        setPage("login");
      }
    })();
  }, []);

  if (page === "login") return <Login {...nav} />;

  if (page === "dashboard") return <Dashboard {...nav} />;
  if (page === "colaboradores") return <Colaboradores {...nav} />;
  if (page === "automatizacion") return <Automatizacion {...nav} />;
  if (page === "posicionar_firma") return <PosicionarFirma {...nav} onDone={() => setPage("automatizacion")} />;

  if (page === "sql") return <QuerySQL {...nav} />;
  if (page === "nlquery") return <NLQuery {...nav} />;

  return <Dashboard {...nav} />;
}
