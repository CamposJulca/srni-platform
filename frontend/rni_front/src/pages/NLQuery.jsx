// src/pages/NLQuery.jsx
import { useEffect, useState } from "react";
import AppLayout from "../layouts/AppLayout";
import { logout, me } from "../api/auth";
import { nlqHealth, nlqSchema, nlqRun, nlqGenerateSQL } from "../api/nlquery";
import "../assets/nlquery.css";
import HelpModal from "../components/HelpModal";

function Table({ columns, rows }) {
  if (!columns?.length) return null;
  return (
    <div className="nlq-table-wrapper">
      <table className="nlq-table">
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

export default function NLQuery({
  onGoHome,
  onGoDashboard,
  onGoSql,
  onGoColaboradores,
  onGoAutomatizacion,
  onGoNLQuery,
  onLogout,
}) {
  const [username, setUsername] = useState("Usuario");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const [health, setHealth] = useState(null);
  const [schema, setSchema] = useState(null);

  const [question, setQuestion] = useState("");
  const [sql, setSql] = useState("SELECT 1 as ok");

  const [result, setResult] = useState({ columns: [], rows: [] });
  const [helpOpen, setHelpOpen] = useState(false);

  async function refresh() {
    const [h, s] = await Promise.all([nlqHealth(), nlqSchema()]);
    setHealth(h);
    setSchema(s);
  }

  useEffect(() => {
    (async () => {
      try {
        const u = await me();
        setUsername(u?.username || "Usuario");
      } catch {
        setUsername("Usuario");
      }
      try {
        await refresh();
      } catch {
        // ignore
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

  async function runSQL() {
    setBusy(true);
    setError("");
    try {
      const data = await nlqRun({ sql });
      const r = data?.result || data?.result_set || data?.resultados || {};
      setResult({
        columns: r.columns || data?.columns || [],
        rows: r.rows || data?.rows || [],
      });
    } catch (e) {
      setResult({ columns: [], rows: [] });
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function generateSQL() {
    setBusy(true);
    setError("");
    try {
      const data = await nlqGenerateSQL(question);
      const newSql = data?.sql || data?.generated_sql;
      if (!newSql) throw new Error("No se recibió SQL generado.");
      setSql(newSql);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function runQuestion() {
    setBusy(true);
    setError("");
    try {
      const data = await nlqRun({ question });
      const r = data?.result || {};
      if (data?.sql) setSql(data.sql);
      setResult({
        columns: r.columns || data?.columns || [],
        rows: r.rows || data?.rows || [],
      });
    } catch (e) {
      setResult({ columns: [], rows: [] });
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  const openaiReady = health?.openai_configured === true;

  return (
    <AppLayout
      title="NLQuery – RNI"
      username={username}
      onLogout={handleLogout}
      onGoHome={onGoHome}
      onGoDashboard={onGoDashboard}
      onGoSql={onGoSql}
      onGoColaboradores={onGoColaboradores}
      onGoAutomatizacion={onGoAutomatizacion}
      onGoNLQuery={onGoNLQuery}
    >
      <div className="nlq-header">
        <div className="nlq-header-row">
          <div>
            <h2>NLQuery (NL → SQL)</h2>
            <p>Modo manual (SQL) funciona siempre. Modo pregunta requiere OpenAI configurado.</p>
          </div>

          <button className="nlq-btn secondary" type="button" onClick={() => setHelpOpen(true)}>
            Ayuda
          </button>
        </div>
      </div>

      <div className="nlq-badges">
        <span className={`nlq-badge ${health?.db_ok ? "ok" : "err"}`}>DB</span>
        <span className={`nlq-badge ${health?.schema_ok ? "ok" : "err"}`}>SCHEMA</span>
        <span className={`nlq-badge ${openaiReady ? "ok" : "warn"}`}>OPENAI</span>
      </div>

      {error && <div className="nlq-error"><b>Error:</b> {error}</div>}

      <div className="nlq-grid">
        <div className="nlq-card">
          <h3>Pregunta (opcional)</h3>
          <textarea
            className="nlq-textarea"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder='Ej: "Muéstrame 20 colaboradores activos"'
          />

          <div className="nlq-actions">
            <button
              className="nlq-btn"
              type="button"
              onClick={generateSQL}
              disabled={busy || !question.trim() || !openaiReady}
              title={!openaiReady ? "OPENAI_API_KEY no configurada en backend" : ""}
            >
              Generar SQL
            </button>

            <button
              className="nlq-btn"
              type="button"
              onClick={runQuestion}
              disabled={busy || !question.trim() || !openaiReady}
              title={!openaiReady ? "OPENAI_API_KEY no configurada en backend" : ""}
            >
              NL → SQL → Run
            </button>

            <button className="nlq-btn secondary" type="button" onClick={refresh} disabled={busy}>
              Refrescar
            </button>
          </div>

          {!openaiReady && (
            <div className="nlq-hint">
              OPENAI no está configurado. Puedes usar el modo SQL manual mientras.
            </div>
          )}
        </div>

        <div className="nlq-card">
          <h3>SQL manual (seguro)</h3>
          <textarea
            className="nlq-textarea"
            value={sql}
            onChange={(e) => setSql(e.target.value)}
            placeholder="SELECT 1 as ok"
          />

          <div className="nlq-actions">
            <button className="nlq-btn" type="button" onClick={runSQL} disabled={busy || !sql.trim()}>
              Ejecutar SQL
            </button>
            <button
              className="nlq-btn secondary"
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
      </div>

      <div className="nlq-debug">
        <h3>Debug (schema)</h3>
        <pre>{schema ? JSON.stringify(schema, null, 2) : "Cargando schema..."}</pre>
      </div>

      <HelpModal
        open={helpOpen}
        title="Guía rápida – NLQuery"
        onClose={() => setHelpOpen(false)}
      >
        <div className="hm-section">
          <h4>Modo SQL manual</h4>
          <p>Siempre disponible. Escribes un <b>SELECT</b> y ejecutas.</p>
          <p className="hm-note">Regla: sin “;”.</p>
        </div>

        <div className="hm-section">
          <h4>Modo Pregunta (inteligente)</h4>
          <p>
            Escribes la pregunta en español. El backend genera SQL y (si quieres) lo ejecuta.
          </p>
          <p className="hm-note">
            Si OPENAI está en amarillo, falta configurar <b>OPENAI_API_KEY</b> en el backend.
          </p>
        </div>

        <div className="hm-section">
          <h4>Ejemplos de preguntas útiles</h4>
          <div className="hm-code">{`- "Muéstrame 20 colaboradores activos"
- "Busca colaborador por cédula 79996063"
- "Contratos que vencen en los próximos 30 días"
- "Top 10 colaboradores con más actividades"`}</div>
        </div>

        <div className="hm-section">
          <h4>Qué puede consultar</h4>
          <p>Solo lo que exista en el schema permitido del sistema (whitelist).</p>
        </div>
      </HelpModal>
    </AppLayout>
  );
}
