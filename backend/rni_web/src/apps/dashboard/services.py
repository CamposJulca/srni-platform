from django.db import connection


def _table_exists(table_name: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("SELECT to_regclass(%s);", [table_name])
        return cursor.fetchone()[0] is not None


def _t(name: str) -> str:
    """
    Resuelve nombre de tabla según exista:
    - primero intenta sin sufijo
    - luego con sufijo _core
    """
    if _table_exists(name):
        return name
    if _table_exists(f"{name}_core"):
        return f"{name}_core"
    return name  # fallback para que el error sea claro si falta


def fetch_kpis_generales():
    """
    KPIs generales.
    Nota: contrato_core NO tiene columna de valor/monto, así que
    valor_total_contratado queda en 0 hasta que exista una tabla/columna monetaria real.
    """
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT COUNT(*) FROM "{_t("colaborador")}";')
        total_colaboradores = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT COUNT(*)
            FROM "{_t("colaborador")}"
            WHERE UPPER(estado) = 'ACTIVO';
        """)
        colaboradores_activos = cursor.fetchone()[0]

        cursor.execute(f'SELECT COUNT(*) FROM "{_t("contrato")}";')
        total_contratos = cursor.fetchone()[0]

        valor_total_contratado = 0

    return {
        "total_colaboradores": total_colaboradores,
        "colaboradores_activos": colaboradores_activos,
        "total_contratos": total_contratos,
        "valor_total_contratado": valor_total_contratado,
    }


def fetch_colaboradores_por_equipo():
    """
    Distribución de colaboradores por equipo.
    Si la tabla/relación no existe en el dump, retorna vacío sin romper.
    """
    if not _table_exists(_t("equipo")) or not _table_exists(_t("colaborador")):
        return {"equipos_labels": [], "equipos_data": []}

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT
                e.nombre AS equipo,
                COUNT(c.id) AS total
            FROM "{_t("equipo")}" e
            LEFT JOIN "{_t("colaborador")}" c ON c.equipo_id = e.id
            GROUP BY e.nombre
            ORDER BY total DESC;
        """)
        rows = cursor.fetchall()

    return {
        "equipos_labels": [r[0] for r in rows],
        "equipos_data": [r[1] for r in rows],
    }


def fetch_top_actividades_por_colaborador(limit=10):
    """
    Top-N de colaboradores con mayor número de actividades.

    Confirmado en DB:
    - actividad existe (sin _core)
    - colaborador es colaborador_core (o sin sufijo si algún día existe)
    """
    if not _table_exists("actividad") or not _table_exists(_t("colaborador")):
        return {"actividades_top_labels": [], "actividades_top_data": []}

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT
                c.nombres AS colaborador,
                COUNT(a.id) AS total
            FROM "{_t("colaborador")}" c
            LEFT JOIN "actividad" a ON a.colaborador_id = c.id
            GROUP BY c.nombres
            ORDER BY total DESC
            LIMIT %s;
        """, [limit])
        rows = cursor.fetchall()

    return {
        "actividades_top_labels": [r[0] for r in rows],
        "actividades_top_data": [r[1] for r in rows],
    }


def fetch_dashboard_kpis(limit_top=10):
    kpis = fetch_kpis_generales()
    equipos = fetch_colaboradores_por_equipo()
    actividades = fetch_top_actividades_por_colaborador(limit=limit_top)

    return {
        **kpis,
        "equipos": {
            "labels": equipos.get("equipos_labels", []),
            "data": equipos.get("equipos_data", []),
        },
        "actividades_top": {
            "labels": actividades.get("actividades_top_labels", []),
            "data": actividades.get("actividades_top_data", []),
        },
    }
