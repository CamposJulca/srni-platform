document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       Fila 1 – Gráfica KPIs generales
    ===================================================== */

    const kpiCanvas = document.getElementById("kpiChart");

    if (kpiCanvas) {

        const totalColaboradores = parseInt(kpiCanvas.dataset.totalColaboradores);
        const colaboradoresActivos = parseInt(kpiCanvas.dataset.colaboradoresActivos);
        const totalContratos = parseInt(kpiCanvas.dataset.totalContratos);

        const ctxKpi = kpiCanvas.getContext("2d");

        new Chart(ctxKpi, {
            type: "bar",
            data: {
                labels: [
                    "Total colaboradores",
                    "Colaboradores activos",
                    "Contratos"
                ],
                datasets: [{
                    label: "KPIs generales",
                    data: [
                        totalColaboradores,
                        colaboradoresActivos,
                        totalContratos
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }

    /* =====================================================
       Fila 2 – Distribución de colaboradores por equipo
    ===================================================== */

    const equipoCanvas = document.getElementById("equipoChart");

    if (equipoCanvas) {

        const labels = JSON.parse(equipoCanvas.dataset.labels);
        const values = JSON.parse(equipoCanvas.dataset.values);

        const ctxEquipo = equipoCanvas.getContext("2d");

        new Chart(ctxEquipo, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Colaboradores por equipo",
                    data: values,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }

    /* =====================================================
        Fila 3 – Top 10 actividades por colaborador
        ===================================================== */

        const actividadCanvas = document.getElementById("actividadChart");

        if (actividadCanvas) {

            const labels = JSON.parse(actividadCanvas.dataset.labels);
            const values = JSON.parse(actividadCanvas.dataset.values);

            const ctxActividad = actividadCanvas.getContext("2d");

            new Chart(ctxActividad, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Número de actividades",
                        data: values,
                        borderWidth: 1
                    }]
                },
                options: {
                    indexAxis: 'y',   // 🔑 barras horizontales
                    responsive: true,
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            });
        }


});
