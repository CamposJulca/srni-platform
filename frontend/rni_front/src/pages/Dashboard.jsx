import { useEffect, useRef, useState } from "react";
import Chart from "chart.js/auto";
import AppLayout from "../layouts/AppLayout";
import { getKpis } from "../api/dashboard";
import { logout, me } from "../api/auth";

export default function Dashboard({
  onGoHome,
  onGoDashboard,
  onGoSql,
  onGoColaboradores,
  onGoAutomatizacion,
  onLogout,
}) {
  const [data, setData] = useState(null);
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(true);

  const kpiChartRef = useRef(null);
  const equipoChartRef = useRef(null);
  const actividadChartRef = useRef(null);

  const kpiChart = useRef(null);
  const equipoChart = useRef(null);
  const actividadChart = useRef(null);

  useEffect(() => {
    (async () => {
      try {
        const [kpis, meData] = await Promise.all([getKpis(10), me()]);
        setData(kpis);
        setUser(meData);
      } catch (e) {
        setError("No se pudo cargar el dashboard");
      } finally {
        setBusy(false);
      }
    })();
  }, []);

  useEffect(() => {
    if (!data) return;

    kpiChart.current?.destroy();
    equipoChart.current?.destroy();
    actividadChart.current?.destroy();

    kpiChart.current = new Chart(kpiChartRef.current, {
      type: "bar",
      data: {
        labels: ["Total colaboradores", "Activos", "Contratos"],
        datasets: [
          {
            data: [
              data.total_colaboradores,
              data.colaboradores_activos,
              data.total_contratos,
            ],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
      },
    });

    equipoChart.current = new Chart(equipoChartRef.current, {
      type: "pie",
      data: {
        labels: data.equipos.labels.length ? data.equipos.labels : ["Sin datos"],
        datasets: [
          {
            data: data.equipos.data.length ? data.equipos.data : [1],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    });

    actividadChart.current = new Chart(actividadChartRef.current, {
      type: "bar",
      data: {
        labels: data.actividades_top.labels,
        datasets: [
          {
            data: data.actividades_top.data,
          },
        ],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
      },
    });
  }, [data]);

  async function handleLogout() {
    try {
      await logout();
    } finally {
      onLogout?.();
    }
  }

  return (
    <AppLayout
      title="Dashboard – Red Nacional de Información"
      username={user?.username || "Usuario"}
      onLogout={handleLogout}
      onGoHome={onGoHome}
      onGoDashboard={onGoDashboard}
      onGoSql={onGoSql}
      onGoColaboradores={onGoColaboradores}
      onGoAutomatizacion={onGoAutomatizacion}
    >
      {busy && <p>Cargando...</p>}
      {error && <p style={{ color: "#b71c1c" }}>{error}</p>}

      {!busy && data && (
        <>
          <h2>Métricas generales</h2>

          <div className="kpi-container">
            <div className="kpi-card">
              <div className="kpi-title">Total de colaboradores</div>
              <div className="kpi-value">{data.total_colaboradores}</div>
            </div>
            <div className="kpi-card">
              <div className="kpi-title">Colaboradores activos</div>
              <div className="kpi-value">{data.colaboradores_activos}</div>
            </div>
            <div className="kpi-card">
              <div className="kpi-title">Total de contratos</div>
              <div className="kpi-value">{data.total_contratos}</div>
            </div>
            <div className="kpi-card">
              <div className="kpi-title">Valor total contratado</div>
              <div className="kpi-value">
                ${Number(data.valor_total_contratado || 0).toLocaleString()}
              </div>
            </div>
          </div>

          <hr />

          <h2>Resumen gráfico</h2>
          <div className="chart-container">
            <div className="chart-fixed">
              <canvas ref={kpiChartRef} />
            </div>
          </div>

          <hr />

          <h2>Distribución de colaboradores por equipo</h2>
          <div className="chart-container">
            <div className="chart-fixed">
              <canvas ref={equipoChartRef} />
            </div>
          </div>

          <hr />

          <h2>Carga operativa – Top 10 colaboradores</h2>
          <div className="chart-container">
            <div className="chart-fixed tall">
              <canvas ref={actividadChartRef} />
            </div>
          </div>
        </>
      )}
    </AppLayout>
  );
}
