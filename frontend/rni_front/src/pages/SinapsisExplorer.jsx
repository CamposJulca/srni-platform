import data from "../data/sinapsis/projects_snapshot_2026-01-19.json";

export default function SinapsisExplorer() {
  const first = data[0];

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Sinapsis – Explorador de Proyectos</h1>

      <p><strong>Total de proyectos:</strong> {data.length}</p>

      <h2>Claves del proyecto</h2>
      <ul>
        {Object.keys(first).map((k) => (
          <li key={k}>{k}</li>
        ))}
      </ul>

      <h2>Primer proyecto (raw)</h2>
      <pre style={{ maxHeight: "400px", overflow: "auto", background: "#111", color: "#0f0" }}>
        {JSON.stringify(first, null, 2)}
      </pre>
    </div>
  );
}
