// src/pages/PosicionarFirma.jsx
import { useEffect, useMemo, useRef, useState } from "react";
import AppLayout from "../layouts/AppLayout";
import { logout, me } from "../api/auth";
import {
  autoFirmaPreviewUrlBusted,
  autoHealth,
  autoPreviewPdfUrlBusted,
  autoSaveFirmaPosition,
} from "../api/automatizacion";
import "../assets/posicionar_firma.css";

export default function PosicionarFirma({
  onGoHome,
  onGoDashboard,
  onGoSql,
  onGoColaboradores,
  onGoAutomatizacion,
  onLogout,
  onDone,
}) {
  const [username, setUsername] = useState("Usuario");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const [firmaUrl, setFirmaUrl] = useState(autoFirmaPreviewUrlBusted());
  const [pdfUrl, setPdfUrl] = useState(autoPreviewPdfUrlBusted());
  const [hasPdf, setHasPdf] = useState(false);

  const [canContinue, setCanContinue] = useState(false);

  const sheetRef = useRef(null);
  const drag = useRef({ on: false, dx: 0, dy: 0 });
  const resizing = useRef({ on: false, startX: 0, startY: 0, startW: 0, startH: 0 });

  const [box, setBox] = useState({ left: 40, top: 40, width: 180, height: 80 });

  useEffect(() => {
    (async () => {
      try {
        const u = await me();
        setUsername(u?.username || "Usuario");
      } catch {
        setUsername("Usuario");
      }
    })();

    (async () => {
      try {
        const h = await autoHealth();
        const ok = !!h?.has_zip && !!h?.has_signature_image && (h?.pdf_count ?? 0) > 0;
        setHasPdf(ok);
        if (!h?.has_zip || !h?.has_signature_image) {
          setError("Primero debes cargar ZIP y firma antes de posicionar.");
        } else if ((h?.pdf_count ?? 0) === 0) {
          setError("No hay PDF preview. Vuelve a Automatización y genera el preview (paso 1).");
        } else {
          setError("");
        }
      } catch {
        // nada
      }
    })();
  }, []);

  function onMouseDownFirma(e) {
    if (e.target?.classList?.contains("resize-handle")) return;
    drag.current.on = true;
    drag.current.dx = e.clientX - box.left;
    drag.current.dy = e.clientY - box.top;
  }

  function onMouseMove(e) {
    const sheet = sheetRef.current?.getBoundingClientRect();
    if (!sheet) return;

    if (drag.current.on) {
      const newLeft = e.clientX - drag.current.dx;
      const newTop = e.clientY - drag.current.dy;

      const maxLeft = sheet.width - box.width;
      const maxTop = sheet.height - box.height;

      setBox((b) => ({
        ...b,
        left: Math.max(0, Math.min(newLeft, maxLeft)),
        top: Math.max(0, Math.min(newTop, maxTop)),
      }));
      return;
    }

    if (resizing.current.on) {
      const dx = e.clientX - resizing.current.startX;
      const dy = e.clientY - resizing.current.startY;

      const newW = Math.max(60, Math.min(resizing.current.startW + dx, sheet.width - box.left));
      const newH = Math.max(30, Math.min(resizing.current.startH + dy, sheet.height - box.top));

      setBox((b) => ({ ...b, width: newW, height: newH }));
    }
  }

  function onMouseUp() {
    drag.current.on = false;
    resizing.current.on = false;
  }

  function onMouseDownResize(e) {
    e.stopPropagation();
    resizing.current.on = true;
    resizing.current.startX = e.clientX;
    resizing.current.startY = e.clientY;
    resizing.current.startW = box.width;
    resizing.current.startH = box.height;
  }

  const ratios = useMemo(() => {
    const sheet = sheetRef.current?.getBoundingClientRect();
    if (!sheet) return null;

    const x_ratio = box.left / sheet.width;
    const y_ratio = (sheet.height - (box.top + box.height)) / sheet.height;
    const width_ratio = box.width / sheet.width;
    const height_ratio = box.height / sheet.height;

    return {
      page: 1,
      x_ratio: Number(x_ratio.toFixed(6)),
      y_ratio: Number(y_ratio.toFixed(6)),
      width_ratio: Number(width_ratio.toFixed(6)),
      height_ratio: Number(height_ratio.toFixed(6)),
    };
  }, [box]);

  async function handleSave() {
    setBusy(true);
    setError("");
    try {
      if (!ratios) throw new Error("No se pudo calcular la posición.");
      await autoSaveFirmaPosition(ratios);
      setCanContinue(true);
    } catch (e) {
      setError(e.message);
      setCanContinue(false);
    } finally {
      setBusy(false);
    }
  }

  async function handleLogout() {
    try {
      await logout();
    } finally {
      onLogout?.();
    }
  }

  return (
    <AppLayout
      title="Seleccionar posición de firma"
      username={username}
      onLogout={handleLogout}
      onGoHome={onGoHome}
      onGoDashboard={onGoDashboard}
      onGoSql={onGoSql}
      onGoColaboradores={onGoColaboradores}
      onGoAutomatizacion={onGoAutomatizacion}
    >
      <div className="pf-header">
        <h2>Seleccionar posición de la firma</h2>
        <p>Arrastra y ajusta la firma exactamente donde debe ir</p>
      </div>

      {error && <div className="pf-error">{error}</div>}

      <div className="pf-layout" onMouseMove={onMouseMove} onMouseUp={onMouseUp}>
        <div className="pf-sheet" ref={sheetRef}>
          {/* PDF preview de fondo */}
          {hasPdf ? (
            <iframe
              title="PDF Preview"
              className="pf-pdf"
              src={pdfUrl}
            />
          ) : (
            <div className="pf-no-pdf">
              No hay PDF preview todavía.
            </div>
          )}

          {/* Firma encima */}
          <div
            className="pf-firma"
            style={{
              left: `${box.left}px`,
              top: `${box.top}px`,
              width: `${box.width}px`,
              height: `${box.height}px`,
            }}
            onMouseDown={onMouseDownFirma}
          >
            <img src={firmaUrl} alt="Firma" />
            <div className="resize-handle" onMouseDown={onMouseDownResize} />
          </div>
        </div>

        <aside className="pf-controls">
          <p><b>Instrucciones:</b></p>
          <ol>
            <li>Arrastra la firma</li>
            <li>Ajusta tamaño (esquina inferior derecha)</li>
            <li>Guarda la posición</li>
          </ol>

          <button className="pf-btn" type="button" onClick={handleSave} disabled={busy || !hasPdf}>
            Guardar posición
          </button>

          <button className="pf-btn" type="button" onClick={() => onDone?.()} disabled={!canContinue}>
            Continuar
          </button>

          <button className="pf-btn secondary" type="button" onClick={() => onDone?.()}>
            Cancelar
          </button>

          <button
            className="pf-btn secondary"
            type="button"
            onClick={() => {
              setPdfUrl(autoPreviewPdfUrlBusted());
              setFirmaUrl(autoFirmaPreviewUrlBusted());
            }}
          >
            Refrescar preview
          </button>

          <p className="pf-note">Ratios (enviar al backend)</p>
          <pre className="pf-pre">{ratios ? JSON.stringify(ratios, null, 2) : "Calculando..."}</pre>
        </aside>
      </div>
    </AppLayout>
  );
}
