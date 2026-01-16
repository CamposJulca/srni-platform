import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import (
    fetch_kpis_generales,
    fetch_colaboradores_por_equipo,
    fetch_top_actividades_por_colaborador
)


@login_required
def dashboard_view(request):
    context = {}

    # =========================
    # Fila 1 – KPIs generales
    # =========================
    context.update(fetch_kpis_generales())

    # =========================
    # Fila 2 – Distribución por equipo
    # =========================
    equipos = fetch_colaboradores_por_equipo()
    context["equipos_labels"] = json.dumps(equipos["equipos_labels"])
    context["equipos_data"] = json.dumps(equipos["equipos_data"])

    # =========================
    # Fila 3 – Carga operativa (Top 10)
    # =========================
    actividades = fetch_top_actividades_por_colaborador(limit=10)
    context["actividades_labels"] = json.dumps(actividades["actividades_top_labels"])
    context["actividades_data"] = json.dumps(actividades["actividades_top_data"])

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )
