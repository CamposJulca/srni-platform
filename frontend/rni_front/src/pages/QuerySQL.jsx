// src/pages/QuerySQL.jsx
import { useEffect, useState } from "react";
import AppLayout from "../layouts/AppLayout";
import { logout, me } from "../api/auth";
import { analyticsExecuteSQL, analyticsHealth } from "../api/analytics";
import "../assets/query_sql.css";
import HelpModal from "../components/HelpModal";

function Table({ columns, rows }) {
  if (!columns?.length) return null;

  return (
    <div className="qsql-table-wrapper">
      <table className="qsql-table">
        <thead>
          <tr>
            {columns.map((c) => (
              <th key={c}>{c}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {(rows || []).map((r, i) => (
            <tr key={i}>
              {r.map((cell, j) => (
                <td key={j}>{cell === null ? "NULL" : String(cell)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function QuerySQL({
  onGoHome,
  onGoDashboard,
  onGoSql,
  onGoColaboradores,
  onGoAutomatizacion,
  onGoNLQuery,
  onLogout,
}) {
  const [username, setUsername] = useState("Usuario");
  const [sql, setSql] = useState("SELECT 1 as ok");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [health, setHealth] = useState(null);
  const [helpOpen, setHelpOpen] = useState(false);

  const [result, setResult] = useState({ columns: [], rows: [] });

  useEffect(() => {
    (async () => {
      try {
        const u = await me();
        setUsername(u?.username || "Usuario");
      } catch {
        setUsername("Usuario");
      }
      try {
        const h = await analyticsHealth();
        setHealth(h);
      } catch {
        setHealth(null);
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

  async function run() {
    setBusy(true);
    setError("");
    try {
      const data = await analyticsExecuteSQL(sql);
      const r = data?.result || {};
      setResult({
        columns: r.columns || [],
        rows: r.rows || [],
      });
    } catch (e) {
      setResult({ columns: [], rows: [] });
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <AppLayout
      title="Query SQL – RNI"
      username={username}
      onLogout={handleLogout}
      onGoHome={onGoHome}
      onGoDashboard={onGoDashboard}
      onGoSql={onGoSql}
      onGoColaboradores={onGoColaboradores}
      onGoAutomatizacion={onGoAutomatizacion}
      onGoNLQuery={onGoNLQuery}
    >
      <div className="qsql-header">
        <div className="qsql-header-row">
          <div>
            <h2>Consulta SQL – PostgreSQL</h2>
            <p>Solo permite SELECT. Solo superusers pueden ejecutar.</p>
          </div>

          <button
            className="qsql-btn secondary"
            type="button"
            onClick={() => setHelpOpen(true)}
          >
            Ayuda
          </button>
        </div>
      </div>

      {health?.db_ok === true && <div className="qsql-pill ok">DB OK</div>}
      {health?.db_ok === false && <div className="qsql-pill err">DB ERROR</div>}

      {error && (
        <div className="qsql-error">
          <b>Error:</b> {error}
        </div>
      )}

      <div className="qsql-card">
        <textarea
          value={sql}
          onChange={(e) => setSql(e.target.value)}
          placeholder="SELECT 1 as ok"
          className="qsql-textarea"
        />

        <div className="qsql-actions">
          <button
            className="qsql-btn"
            type="button"
            onClick={run}
            disabled={busy || !sql.trim()}
          >
            Consultar
          </button>

          <button
            className="qsql-btn secondary"
            type="button"
            onClick={() => {
              setSql("SELECT 1 as ok");
              setResult({ columns: [], rows: [] });
              setError("");
            }}
            disabled={busy}
          >
            Limpiar
          </button>
        </div>

        <Table columns={result.columns} rows={result.rows} />
      </div>

      <HelpModal
        open={helpOpen}
        title="Guía rápida – Query SQL"
        onClose={() => setHelpOpen(false)}
      >
        <div className="hm-section">
          <h4>Qué puedes hacer</h4>
          <p>Consultar datos con <b>SELECT</b> únicamente. No modifica nada.</p>
        </div>

        <div className="hm-section">
          <h4>Qué NO puedes hacer</h4>
          <ul>
            <li>No se permiten <b>INSERT / UPDATE / DELETE / DROP / ALTER</b></li>
            <li>No se permite usar <b>;</b> (punto y coma)</li>
          </ul>
          <p className="hm-note">Si usas “;” te dará “Multiple statements are not allowed”.</p>
        </div>

        <div className="hm-section">
          <h4>Ejemplos (Colaboradores)</h4>
          <div className="hm-code">{`-- Por cédula
SELECT cedula, nombres, apellidos, estado, created_at
FROM colaborador
WHERE cedula = '79996063'
LIMIT 50

-- Por estado
SELECT cedula, nombres, apellidos, estado, created_at
FROM colaborador
WHERE estado = 'ACTIVO'
ORDER BY created_at DESC
LIMIT 50

-- Por nombre o apellido
SELECT cedula, nombres, apellidos, estado, created_at
FROM colaborador
WHERE (nombres ILIKE '%DIANA%' OR apellidos ILIKE '%PINO%')
ORDER BY created_at DESC
LIMIT 50`}</div>
          <p className="hm-note">
            Si tu tabla/columnas se llaman distinto, valida con el schema de NLQuery.
          </p>
        </div>
      </HelpModal>
    </AppLayout>
  );
}
