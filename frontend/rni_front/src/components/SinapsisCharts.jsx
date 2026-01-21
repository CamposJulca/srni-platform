import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from "recharts";

const COLORS = ["#4ade80", "#60a5fa", "#facc15", "#f87171", "#a78bfa"];

function countBy(data, key) {
  const map = {};
  data.forEach(item => {
    const value = item[key] ?? "No definido";
    map[value] = (map[value] || 0) + 1;
  });
  return Object.entries(map).map(([name, value]) => ({ name, value }));
}

export default function SinapsisCharts({ projects }) {
  const byStatus = countBy(projects, "status");
  const byLifecycle = countBy(projects, "lifecycle_stage");
  const byRisk = countBy(projects, "risk_level");

  return (
    <div style={{ display: "grid", gap: "2rem", marginTop: "2rem" }}>

      {/* Estado */}
      <section>
        <h3>Proyectos por Estado</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={byStatus}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#60a5fa" />
          </BarChart>
        </ResponsiveContainer>
      </section>

      {/* Ciclo de vida */}
      <section>
        <h3>Proyectos por Ciclo de Vida</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie data={byLifecycle} dataKey="value" nameKey="name" label>
              {byLifecycle.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </section>

      {/* Riesgo */}
      <section>
        <h3>Proyectos por Nivel de Riesgo</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={byRisk}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#f87171" />
          </BarChart>
        </ResponsiveContainer>
      </section>

    </div>
  );
}
