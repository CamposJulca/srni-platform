from django.db.models import Count

from apps.colaboradores.models import (
    ColaboradorCore,
    ContratoCore,
    ColaboradorContrato,
)


def fetch_kpis_generales():
    """
    KPIs generales basados en tablas reales del dump.
    """

    total_colaboradores = ColaboradorCore.objects.count()

    colaboradores_activos = ColaboradorCore.objects.filter(
        estado__iexact="Activo"
    ).count()

    total_contratos = ContratoCore.objects.count()

    # No existe campo 'valor' en ContratoCore (según tu model).
    # KPI estable: total de vinculaciones colaborador-contrato
    total_vinculaciones = ColaboradorContrato.objects.count()

    return {
        "total_colaboradores": total_colaboradores,
        "colaboradores_activos": colaboradores_activos,
        "total_contratos": total_contratos,
        "valor_total_contratado": 0,  # Mantengo la key para no romper el template
        "total_vinculaciones": total_vinculaciones,  # Nueva métrica útil
    }


def fetch_colaboradores_por_equipo():
    """
    No hay 'Equipo' en tu dump/modelo actual.
    Devolvemos vacío para que el frontend no se caiga.
    """
    return {"equipos_labels": [], "equipos_data": []}


def fetch_top_actividades_por_colaborador(limit=10):
    """
    No hay 'Actividad' modelada en tu dump/modelo actual.
    KPI equivalente: Top colaboradores con más contratos vinculados.
    """

    qs = (
        ColaboradorCore.objects
        .annotate(total=Count("vinculos"))
        .order_by("-total")[:limit]
    )

    labels = [f"{c.nombres} {c.apellidos}" for c in qs]
    data = [c.total for c in qs]

    return {
        "actividades_top_labels": labels,
        "actividades_top_data": data,
    }
