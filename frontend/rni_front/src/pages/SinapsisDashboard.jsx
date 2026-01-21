import { useEffect, useState } from "react";
import { fetchProjects } from "../api/sinapsisApi";

export default function SinapsisDashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProjects()
      .then(setProjects)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Cargando proyectos SINAPSIS…</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div style={{ padding: "1rem" }}>
      <h1>Dashboard SINAPSIS</h1>
      <p>Total proyectos: {projects.length}</p>

      <table border="1" cellPadding="6">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Estado</th>
            <th>Ciclo</th>
            <th>Riesgo</th>
            <th>Iniciativa</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((p, i) => (
            <tr key={i}>
              <td>{p.name}</td>
              <td>{p.status}</td>
              <td>{p.lifecycle_stage ?? "—"}</td>
              <td>{p.risk_level ?? "—"}</td>
              <td>{p.initiative_level ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
