from django.db import connection


def fetch_kpis_generales():
    """
    Obtiene KPIs agregados para la fila 1 del dashboard.
    Retorna un diccionario listo para la vista.
    """
    with connection.cursor() as cursor:

        # Total colaboradores
        cursor.execute("SELECT COUNT(*) FROM colaborador;")
        total_colaboradores = cursor.fetchone()[0]

        # Colaboradores activos
        cursor.execute("""
            SELECT COUNT(*) 
            FROM colaborador 
            WHERE estado = 'Activo';
        """)
        colaboradores_activos = cursor.fetchone()[0]

        # Total contratos
        cursor.execute("SELECT COUNT(*) FROM contrato;")
        total_contratos = cursor.fetchone()[0]

        # Valor total contratado
        cursor.execute("""
            SELECT COALESCE(SUM(valor), 0)
            FROM contrato;
        """)
        valor_total_contratado = cursor.fetchone()[0]

    return {
        "total_colaboradores": total_colaboradores,
        "colaboradores_activos": colaboradores_activos,
        "total_contratos": total_contratos,
        "valor_total_contratado": valor_total_contratado,
    }

def fetch_colaboradores_por_equipo():
    """
    Retorna la distribución de colaboradores por equipo.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                e.nombre AS equipo,
                COUNT(c.id) AS total
            FROM equipo e
            LEFT JOIN colaborador c ON c.equipo_id = e.id
            GROUP BY e.nombre
            ORDER BY total DESC;
        """)
        rows = cursor.fetchall()

    labels = [row[0] for row in rows]
    data = [row[1] for row in rows]

    return {
        "equipos_labels": labels,
        "equipos_data": data,
    }

def fetch_top_actividades_por_colaborador(limit=10):
    """
    Retorna el Top-N de colaboradores con mayor número de actividades.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                c.nombre AS colaborador,
                COUNT(a.id) AS total
            FROM colaborador c
            LEFT JOIN actividad a ON a.colaborador_id = c.id
            GROUP BY c.nombre
            ORDER BY total DESC
            LIMIT %s;
        """, [limit])
        rows = cursor.fetchall()

    labels = [row[0] for row in rows]
    data = [row[1] for row in rows]

    return {
        "actividades_top_labels": labels,
        "actividades_top_data": data,
    }
