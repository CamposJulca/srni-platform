// src/pages/Automatizacion.jsx
import { useEffect, useMemo, useState } from "react";
import AppLayout from "../layouts/AppLayout";
import { logout, me } from "../api/auth";
import {
  autoDownload,
  autoGenerate,
  autoHealth,
  autoPreviewConvert,
  autoPreviewInfo,
  autoUpload,
} from "../api/automatizacion";
import "../assets/automatizacion.css";

export default function Automatizacion({
  onGoHome,
  onGoDashboard,
  onGoSql,
  onGoColaboradores,
  onGoAutomatizacion,
  onLogout,
  onGoPosicionarFirma,
}) {
  const [username, setUsername] = useState("Usuario");

  const [zipFile, setZipFile] = useState(null);
  const [firmaFile, setFirmaFile] = useState(null);

  const [health, setHealth] = useState(null);
  const [preview, setPreview] = useState(null);

  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const [logs, setLogs] = useState(() => [
    { type: "info", msg: "Esperando acciones del usuario…" },
  ]);

  function pushLog(msg, type = "info") {
    setLogs((prev) => [...prev, { type, msg }]);
  }

  function clearLogs() {
    setLogs([{ type: "info", msg: "Logs limpiados por el usuario" }]);
  }

  async function refreshStatus() {
    try {
      const [h, p] = await Promise.all([autoHealth(), autoPreviewInfo()]);
      setHealth(h);
      setPreview(p);
    } catch {
      setHealth(null);
      setPreview(null);
    }
  }

  useEffect(() => {
    (async () => {
      try {
        const u = await me();
        setUsername(u?.username || "Usuario");
      } catch {
        setUsername("Usuario");
      } finally {
        await refreshStatus();
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const canPosicionar = useMemo(() => {
    const hasZip = !!health?.has_zip;
    const hasFirma = !!health?.has_signature_image;
    const hasPreviewPdf = (health?.pdf_count ?? 0) > 0; // Enfoque B: debe existir preview pdf
    return hasZip && hasFirma && hasPreviewPdf;
  }, [health]);

  const hasPosicion = useMemo(() => !!health?.has_signature_config, [health]);

  const canGenerate = useMemo(() => canPosicionar && hasPosicion, [canPosicionar, hasPosicion]);

  const canDownload = useMemo(() => {
    const n = Number(health?.signed_pdf_count || 0);
    return n > 0;
  }, [health]);

  async function handleLogout() {
    try {
      await logout();
    } finally {
      onLogout?.();
    }
  }

  async function handleUpload() {
    setBusy(true);
    setError("");
    pushLog("Cargando ZIP y firma…", "info");

    try {
      const data = await autoUpload({ zipFile, firmaFile });
      pushLog(`ZIP procesado (${data?.total_docx ?? "?"} documentos)`, "ok");

      pushLog("Generando PDF preview (1 documento)…", "info");
      await autoPreviewConvert();
      pushLog("PDF preview listo", "ok");

      await refreshStatus();
    } catch (e) {
      setError(e.message);
      pushLog(e.message, "error");
    } finally {
      setBusy(false);
    }
  }

  async function handleGenerate() {
    setBusy(true);
    setError("");
    pushLog("Generando y firmando PDFs…", "info");

    try {
      const data = await autoGenerate();
      pushLog(`Proceso completado (PDFs firmados: ${data?.pdf_signed ?? "?"})`, "ok");
      await refreshStatus();
    } catch (e) {
      setError(e.message);
      pushLog(e.message, "error");
    } finally {
      setBusy(false);
    }
  }

  async function handleDownload() {
    setBusy(true);
    setError("");
    pushLog("Descargando ZIP final…", "info");

    try {
      const { blob, filename } = await autoDownload();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      pushLog("ZIP descargado correctamente", "ok");
    } catch (e) {
      setError(e.message);
      pushLog(e.message, "error");
    } finally {
      setBusy(false);
    }
  }

  return (
    <AppLayout
      title="Automatización Documental – RNI"
      username={username}
      onLogout={handleLogout}
      onGoHome={onGoHome}
      onGoDashboard={onGoDashboard}
      onGoSql={onGoSql}
      onGoColaboradores={onGoColaboradores}
      onGoAutomatizacion={onGoAutomatizacion}
    >
      <div className="auto-header">
        <h2>Automatización Documental</h2>
        <p>Firma y generación masiva de documentos en PDF</p>
      </div>

      {error && <div className="auto-error">{error}</div>}

      <div className="auto-grid">
        <div className="auto-steps">
          <section className="auto-step">
            <h3>1. Cargar documentos y firma</h3>

            <label className="auto-label">
              ZIP con documentos (.zip)
              <input type="file" accept=".zip" onChange={(e) => setZipFile(e.target.files?.[0] || null)} />
            </label>

            <label className="auto-label">
              Firma digital (PNG)
              <input type="file" accept="image/png" onChange={(e) => setFirmaFile(e.target.files?.[0] || null)} />
            </label>

            <p className="auto-note">⚠️ La firma debe ser PNG</p>

            <button className="auto-btn" type="button" onClick={handleUpload} disabled={busy || !zipFile || !firmaFile}>
              Cargar ZIP
            </button>

            <p className={`auto-status ${health?.has_zip ? "ok" : ""}`}>
              {health?.has_zip ? "ZIP cargado" : "Pendiente"}
            </p>

            <p className={`auto-status ${(health?.pdf_count ?? 0) > 0 ? "ok" : ""}`}>
              {(health?.pdf_count ?? 0) > 0 ? "PDF preview listo" : "PDF preview pendiente"}
            </p>
          </section>

          <section className="auto-step">
            <h3>2. Seleccionar posición de firma</h3>
            <p className="auto-note">Enfoque B: aquí ya se ve un PDF preview como fondo.</p>

            <button
              className="auto-btn"
              type="button"
              disabled={busy || !canPosicionar}
              onClick={() => {
                pushLog("Abriendo pantalla de posicionamiento de firma", "info");
                onGoPosicionarFirma?.();
              }}
            >
              Seleccionar posición de firma
            </button>

            <p className={`auto-status ${hasPosicion ? "ok" : ""}`}>
              {hasPosicion ? "Firma posicionada" : "Pendiente"}
            </p>
          </section>

          <section className="auto-step">
            <h3>3. Generar y firmar PDFs</h3>
            <button className="auto-btn" type="button" disabled={busy || !canGenerate} onClick={handleGenerate}>
              Generar y firmar PDFs
            </button>

            <p className={`auto-status ${canDownload ? "ok" : ""}`}>
              {canDownload ? "PDFs firmados listos" : "Pendiente"}
            </p>
          </section>

          <section className="auto-step">
            <h3>4. Descargar ZIP final</h3>
            <button className="auto-btn" type="button" disabled={busy || !canDownload} onClick={handleDownload}>
              Descargar ZIP
            </button>

            <p className={`auto-status ${canDownload ? "ok" : ""}`}>
              {canDownload ? "Listo para descargar" : "Pendiente"}
            </p>
          </section>

          <section className="auto-mini">
            <div className="auto-mini-row">
              <span>DOCX:</span>
              <b>{health?.docx_count ?? 0}</b>
            </div>
            <div className="auto-mini-row">
              <span>PDF (incluye preview):</span>
              <b>{health?.pdf_count ?? 0}</b>
            </div>
            <div className="auto-mini-row">
              <span>Firmados:</span>
              <b>{health?.signed_pdf_count ?? 0}</b>
            </div>

            <button
              className="auto-btn secondary"
              type="button"
              onClick={() => {
                pushLog("Refrescando estado…", "info");
                refreshStatus();
              }}
              disabled={busy}
            >
              Refrescar estado
            </button>
          </section>
        </div>

        <div className="auto-logs">
          <div className="auto-logs-header">
            <h3>● Proceso en ejecución</h3>
            <button className="auto-btn secondary" type="button" onClick={clearLogs}>
              Limpiar logs
            </button>
          </div>

          <div className="auto-log-console">
            {logs.map((l, idx) => (
              <div key={idx} className={`auto-log ${l.type}`}>
                <span className="auto-log-time">[{new Date().toLocaleTimeString()}]</span>{" "}
                {l.msg}
              </div>
            ))}
          </div>
        </div>
      </div>

      {preview && (
        <div className="auto-preview">
          <h3>Preview</h3>
          <pre>{JSON.stringify(preview, null, 2)}</pre>
        </div>
      )}
    </AppLayout>
  );
}
