import { useEffect, useState } from "react";
import AppLayout from "../layouts/AppLayout";
import { logout, me } from "../api/auth";
import SinapsisDashboard from "./SinapsisDashboard";

export default function Sinapsis({
  onGoHome,
  onGoDashboard,
  onGoSql,
  onGoNLQuery,
  onGoColaboradores,
  onGoAutomatizacion,
  onGoSinapsis,
  onLogout,
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
      onLogout?.();
    }
  }

  return (
    <AppLayout
      title="SINAPSIS – RNI"
      username={username}
      onLogout={handleLogout}
      onGoHome={onGoHome}
      onGoDashboard={onGoDashboard}
      onGoSql={onGoSql}
      onGoNLQuery={onGoNLQuery}
      onGoColaboradores={onGoColaboradores}
      onGoAutomatizacion={onGoAutomatizacion}
      onGoSinapsis={onGoSinapsis}
    >
      <SinapsisDashboard />
    </AppLayout>
  );
}
