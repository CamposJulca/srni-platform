#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ETL – Carga Excel SRNI 2026 a tabla staging_srni_2026_master
-----------------------------------------------------------
- Lee la PRIMERA hoja del archivo Excel
- Normaliza tipos básicos
- Permite NULLs (POR DEFINIR, cédulas vacías, IDs vacíos)
- Inserta TODO el contenido en PostgreSQL
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from pathlib import Path

# ---------------------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------------------

EXCEL_PATH = Path("../data/SUBDIRECCION RED NACIONAL DE INFORMACION MATRIZ.xlsx")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "srni_actividades",
    "user": "postgres",
    "password": "Alejito10."  # ajusta si aplica
}

TABLE_NAME = "staging_srni_2026_master"

# ---------------------------------------------------------------------
# UTILIDADES
# ---------------------------------------------------------------------

def to_int(value):
    try:
        if pd.isna(value) or str(value).strip() == "":
            return None
        return int(float(value))
    except Exception:
        return None


def to_date(value):
    try:
        if pd.isna(value) or str(value).strip() == "":
            return None
        return pd.to_datetime(value).date()
    except Exception:
        return None


def to_numeric(value):
    try:
        if pd.isna(value) or str(value).strip() == "":
            return None
        return float(
            str(value)
            .replace("$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )
    except Exception:
        return None


def clean_text(value):
    if pd.isna(value):
        return None
    value = str(value).strip()
    return value if value != "" else None


# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------

def main():
    print("=" * 70)
    print("ETL | CARGA STAGING SRNI 2026 MASTER")
    print("=" * 70)

    # --------------------------------------------------
    # 1. Leer Excel
    # --------------------------------------------------
    print("[STEP 1] Leyendo archivo Excel...")
    print(f"[INFO] Archivo: {EXCEL_PATH.resolve()}")

    df = pd.read_excel(EXCEL_PATH, sheet_name=0)
    print(f"[OK] Filas leídas: {len(df)}")

    # --------------------------------------------------
    # 2. Renombrar columnas exactamente como staging
    # --------------------------------------------------
    print("[STEP 2] Normalizando columnas...")

    df = df.rename(columns={
        "ITEM": "item",
        "ID 2026": "id_2026",
        "DEPENDENCIA": "dependencia",
        "DEPENDENCIA ASOCIADA": "dependencia_asociada",
        "NOMBRES CONTRATISTA": "nombres_contratista",
        "APELLIDOS CONTRATISTA": "apellidos_contratista",
        "NUMERO DE CEDULA": "numero_cedula",
        "NIVEL CENTRAL/TERRITORIAL": "nivel_central_territorial",
        "MUNICIPIO EJECUCION": "municipio_ejecucion",
        "DEPARTAMENTO EJECUCION": "departamento_ejecucion",
        "OBJETO PAA": "objeto_paa",
        "REQUSITOS ACADEMICOS": "requisitos_academicos",
        "EXPERIENCIA MINIMA REQUERIDA (MESES)": "experiencia_minima_meses",
        "FECHA ESTIMADA INICIO CONTRATO": "fecha_estimada_inicio",
        "FECHA TERMINACION CONTRATO": "fecha_terminacion",
        "VALOR HONORARIOS MENSUALES ESTIMADOS": "valor_honorarios_mensuales",
        "RUBRO PRESUPUESTAL": "rubro_presupuestal",
        "NIVEL RIESGO ARL": "nivel_riesgo_arl",
        "NOMBRE SUPERVISOR": "nombre_supervisor",
        "CARGO SUPERVISOR": "cargo_supervisor",
        "OBSERVACION": "observacion"
    })

    # --------------------------------------------------
    # 3. Limpieza y casteo
    # --------------------------------------------------
    print("[STEP 3] Limpieza y casteo de datos...")

    records = []

    for _, row in df.iterrows():
        records.append((
            to_int(row.get("item")),
            to_int(row.get("id_2026")),
            clean_text(row.get("dependencia")),
            clean_text(row.get("dependencia_asociada")),
            clean_text(row.get("nombres_contratista")),
            clean_text(row.get("apellidos_contratista")),
            clean_text(row.get("numero_cedula")),

            clean_text(row.get("nivel_central_territorial")),
            clean_text(row.get("municipio_ejecucion")),
            clean_text(row.get("departamento_ejecucion")),

            clean_text(row.get("objeto_paa")),
            clean_text(row.get("requisitos_academicos")),
            to_int(row.get("experiencia_minima_meses")),

            to_date(row.get("fecha_estimada_inicio")),
            to_date(row.get("fecha_terminacion")),

            to_numeric(row.get("valor_honorarios_mensuales")),
            clean_text(row.get("rubro_presupuestal")),
            to_int(row.get("nivel_riesgo_arl")),

            clean_text(row.get("nombre_supervisor")),
            clean_text(row.get("cargo_supervisor")),
            clean_text(row.get("observacion"))
        ))

    print(f"[OK] Registros preparados: {len(records)}")

    # --------------------------------------------------
    # 4. Insertar en PostgreSQL
    # --------------------------------------------------
    print("[STEP 4] Conectando a PostgreSQL...")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("[STEP 5] Limpiando tabla staging...")
    cur.execute(f"TRUNCATE TABLE {TABLE_NAME};")

    insert_sql = f"""
        INSERT INTO {TABLE_NAME} (
            item,
            id_2026,
            dependencia,
            dependencia_asociada,
            nombres_contratista,
            apellidos_contratista,
            numero_cedula,
            nivel_central_territorial,
            municipio_ejecucion,
            departamento_ejecucion,
            objeto_paa,
            requisitos_academicos,
            experiencia_minima_meses,
            fecha_estimada_inicio,
            fecha_terminacion,
            valor_honorarios_mensuales,
            rubro_presupuestal,
            nivel_riesgo_arl,
            nombre_supervisor,
            cargo_supervisor,
            observacion
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, %s, %s
        );
    """

    print("[STEP 6] Insertando datos...")
    execute_batch(cur, insert_sql, records, page_size=100)

    conn.commit()
    cur.close()
    conn.close()

    print("[OK] Inserción completada correctamente")
    print("=" * 70)
    print("FIN DEL PROCESO")
    print("=" * 70)


if __name__ == "__main__":
    main()
