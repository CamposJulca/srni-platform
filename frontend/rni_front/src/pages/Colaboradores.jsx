import { useEffect, useMemo, useState } from "react";
import AppLayout from "../layouts/AppLayout";
import { getColaboradores } from "../api/colaboradores";
import { logout, me } from "../api/auth";
import "../assets/colaboradores.css";

export default function Colaboradores({
  onGoHome,
  onGoDashboard,
  onGoSql,
  onGoColaboradores,
  onGoAutomatizacion,
  onLogout,
}) {
  const [username, setUsername] = useState("Usuario");

  // Filtros UI
  const [q, setQ] = useState("");
  const [estado, setEstado] = useState("");

  // Paginación
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);

  // Data
  const [rows, setRows] = useState([]);
  const [pagination, setPagination] = useState({
    page: 1,
    page_size: 20,
    total: 0,
    total_pages: 1,
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const canPrev = pagination.page > 1;
  const canNext = pagination.page < pagination.total_pages;

  // Para mostrar un resumen arriba
  const summary = useMemo(() => {
    const total = pagination.total || 0;
    const p = pagination.page || 1;
    const tp = pagination.total_pages || 1;
    return `${total} resultados · Página ${p} de ${tp}`;
  }, [pagination]);

  // Cargar usuario una vez
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

  // Cargar lista cuando cambie page, q o estado
  useEffect(() => {
    (async () => {
      setLoading(true);
      setError("");
      try {
        const resp = await getColaboradores({
          page,
          page_size: pageSize,
          q,
          estado,
        });

        setRows(Array.isArray(resp?.items) ? resp.items : []);
        setPagination(
          resp?.pagination || {
            page,
            page_size: pageSize,
            total: 0,
            total_pages: 1,
          }
        );
      } catch (e) {
        setRows([]);
        setPagination({ page: 1, page_size: pageSize, total: 0, total_pages: 1 });
        setError(e?.message || "No se pudo cargar la lista de colaboradores");
      } finally {
        setLoading(false);
      }
    })();
  }, [page, pageSize, q, estado]);

  async function handleLogout() {
    try {
      await logout();
    } finally {
      onLogout?.();
    }
  }

  function handleSearchSubmit(e) {
    e.preventDefault();
    // Cuando se aplica un filtro, se vuelve a la página 1
    setPage(1);
  }

  function handleClear() {
    setQ("");
    setEstado("");
    setPage(1);
  }

  return (
    <AppLayout
      title="Colaboradores – RNI"
      username={username}
      onLogout={handleLogout}
      onGoHome={onGoHome}
      onGoDashboard={onGoDashboard}
      onGoSql={onGoSql}
      onGoColaboradores={onGoColaboradores}
      onGoAutomatizacion={onGoAutomatizacion}
    >
      <div className="colab-header">
        <div>
          <h2 className="colab-h2">Colaboradores</h2>
          <p className="colab-sub">Listado (solo lectura)</p>
        </div>

        <div className="colab-summary">
          {!loading && !error ? summary : ""}
        </div>
      </div>

      {/* FILTROS */}
      <form className="colab-filters" onSubmit={handleSearchSubmit}>
        <div className="filter-group">
          <label className="filter-label">Búsqueda</label>
          <input
            className="filter-input"
            placeholder="Cédula, nombres o apellidos…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>

        <div className="filter-group">
          <label className="filter-label">Estado</label>
          <select
            className="filter-input"
            value={estado}
            onChange={(e) => setEstado(e.target.value)}
          >
            <option value="">Todos</option>
            <option value="ACTIVO">ACTIVO</option>
            <option value="INACTIVO">INACTIVO</option>
          </select>
        </div>

        <div className="filter-actions">
          <button className="btn-primary" type="submit">
            Buscar
          </button>
          <button className="btn-secondary" type="button" onClick={handleClear}>
            Limpiar
          </button>
        </div>
      </form>

      {loading && <p className="colab-muted">Cargando...</p>}
      {error && <div className="colab-error">{error}</div>}

      {!loading && !error && (
        <>
          <div className="colab-table-wrap">
            <table className="colab-table">
              <thead>
                <tr>
                  <th>Cédula</th>
                  <th>Nombres</th>
                  <th>Apellidos</th>
                  <th>Estado</th>
                  <th>Fecha creación</th>
                </tr>
              </thead>

              <tbody>
                {rows.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="colab-muted">
                      Sin datos.
                    </td>
                  </tr>
                ) : (
                  rows.map((c) => (
                    <tr key={c.id}>
                      <td>{c.cedula || "-"}</td>
                      <td>{c.nombres || "-"}</td>
                      <td>{c.apellidos || "-"}</td>
                      <td>
                        <span
                          className={`colab-badge ${String(c.estado || "")
                            .toLowerCase()
                            .trim()}`}
                        >
                          {c.estado || "N/A"}
                        </span>
                      </td>
                      <td>
                        {c.fecha_creacion
                          ? new Date(c.fecha_creacion).toLocaleString()
                          : "-"}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* PAGINACIÓN */}
          <div className="colab-pagination">
            <button
              className="btn-secondary"
              type="button"
              disabled={!canPrev}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
            >
              ← Anterior
            </button>

            <div className="page-indicator">
              Página <b>{pagination.page}</b> de <b>{pagination.total_pages}</b>
            </div>

            <button
              className="btn-secondary"
              type="button"
              disabled={!canNext}
              onClick={() => setPage((p) => Math.min(pagination.total_pages, p + 1))}
            >
              Siguiente →
            </button>
          </div>
        </>
      )}
    </AppLayout>
  );
}
