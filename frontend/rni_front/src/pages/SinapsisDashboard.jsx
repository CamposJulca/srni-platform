import { useEffect, useState } from "react";
import { fetchProjects } from "../api/sinapsisApi";

import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from "recharts";

/* ============================
   Utilidad: conteo por campo
============================ */
function countBy(items, field) {
  const counts = {};
  items.forEach((item) => {
    const key = item?.[field] ?? "No definido";
    counts[key] = (counts[key] || 0) + 1;
  });

  return Object.entries(counts).map(([name, value]) => ({ name, value }));
}

/* ============================
   Paletas
============================ */
const COLORS_STATUS = ["#60a5fa", "#fbbf24", "#f87171", "#a78bfa"];
const COLORS_LIFECYCLE = ["#facc15", "#a78bfa", "#4ade80", "#60a5fa", "#fb7185", "#22c55e"];
const COLORS_RISK = ["#ef4444", "#9ca3af", "#22c55e", "#f97316"];
const COLORS_INITIATIVE = ["#4ade80", "#60a5fa", "#fbbf24", "#9ca3af"];

/* ============================
   Componente
============================ */
export default function SinapsisDashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const data = await fetchProjects();
        // si backend devuelve {ok:true,data:[...]} o solo [...]
        const list = Array.isArray(data) ? data : (data?.data || []);
        setProjects(list);
      } catch (e) {
        setError(e?.message || "Error cargando SINAPSIS");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <p style={{ padding: "1.5rem" }}>Cargando proyectos SINAPSIS…</p>;
  if (error) return <p style={{ padding: "1.5rem" }}>Error: {error}</p>;

  const byStatus = countBy(projects, "status");
  const byLifecycle = countBy(projects, "lifecycle_stage");
  const byRisk = countBy(projects, "risk_level");
  const byInitiative = countBy(projects, "initiative_level");

  return (
    <div style={{ padding: "1.5rem" }}>
      <h1>Dashboard SINAPSIS</h1>
      <p>Total proyectos: {projects.length}</p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(420px, 1fr))",
          gap: "2rem",
          marginTop: "2rem",
        }}
      >
        <section>
          <h3>Proyectos por Estado</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={byStatus}>
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value">
                {byStatus.map((_, i) => (
                  <Cell key={i} fill={COLORS_STATUS[i % COLORS_STATUS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </section>

        <section>
          <h3>Proyectos por Ciclo de Vida</h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={byLifecycle} dataKey="value" nameKey="name" outerRadius={110} label>
                {byLifecycle.map((_, i) => (
                  <Cell key={i} fill={COLORS_LIFECYCLE[i % COLORS_LIFECYCLE.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </section>

        <section>
          <h3>Proyectos por Nivel de Riesgo</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={byRisk}>
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value">
                {byRisk.map((_, i) => (
                  <Cell key={i} fill={COLORS_RISK[i % COLORS_RISK.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </section>

        <section>
          <h3>Proyectos por Nivel de Iniciativa</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={byInitiative}>
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value">
                {byInitiative.map((_, i) => (
                  <Cell key={i} fill={COLORS_INITIATIVE[i % COLORS_INITIATIVE.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </section>
      </div>

      <h3 style={{ marginTop: "3rem" }}>Detalle de proyectos</h3>

      <table border="1" cellPadding="6" style={{ width: "100%", borderCollapse: "collapse" }}>
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
              <td>{p?.name}</td>
              <td>{p?.status}</td>
              <td>{p?.lifecycle_stage ?? "—"}</td>
              <td>{p?.risk_level ?? "—"}</td>
              <td>{p?.initiative_level ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
