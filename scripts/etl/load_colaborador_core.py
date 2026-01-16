# scripts/etl/load_colaborador_core.py

import re
import pandas as pd
from pathlib import Path
from sqlalchemy import text

from .utils_db import get_engine


# ============================================================
# CONFIGURACIÓN
# ============================================================

DATA_DIR = Path("scripts/data")
FILE_NAME = "SRNI_Analisis_Contratistas_20260109_133245.xlsx"
FILE_PATH = DATA_DIR / FILE_NAME

# Puede ser índice (0, 1, 2, ...) o nombre exacto de la hoja
SHEET_NAME = "2. CONSOLIDADO SD RNI"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def extraer_digitos(valor) -> str | None:
    """
    Extrae únicamente los dígitos de un identificador.
    Ejemplos:
        'C.E. 636797' -> '636797'
        '79996063'    -> '79996063'
    """
    if pd.isna(valor):
        return None

    texto = str(valor)
    digitos = re.findall(r"\d+", texto)

    if not digitos:
        return None

    return "".join(digitos)


def split_nombres_apellidos(nombre_completo: str) -> tuple[str, str]:
    """
    Regla institucional:
    - Últimas dos palabras → apellidos
    - Resto → nombres
    """
    if pd.isna(nombre_completo):
        return "", ""

    partes = (
        str(nombre_completo)
        .strip()
        .replace("\n", " ")
        .split()
    )

    if len(partes) < 3:
        return nombre_completo.strip(), ""

    apellidos = " ".join(partes[-2:])
    nombres = " ".join(partes[:-2])

    return nombres, apellidos


# ============================================================
# ETL PRINCIPAL
# ============================================================

def main():
    print("📥 Leyendo archivo Excel...")
    print(f"📄 Archivo: {FILE_PATH.name}")
    print(f"📄 Hoja seleccionada: {SHEET_NAME}")

    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    print(f"📊 Filas leídas: {len(df)}")

    # --------------------------------------------------------
    # Normalización de columnas
    # --------------------------------------------------------
    df = df.rename(columns=str.strip)

    # Validación mínima esperada
    columnas_requeridas = {"CEDULA", "CONTRATISTA"}
    faltantes = columnas_requeridas - set(df.columns)

    if faltantes:
        raise ValueError(f"❌ Columnas faltantes en Excel: {faltantes}")

    # --------------------------------------------------------
    # Limpieza de nombres
    # --------------------------------------------------------
    df["CONTRATISTA"] = (
        df["CONTRATISTA"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    # --------------------------------------------------------
    # Extracción de cédula (solo dígitos)
    # --------------------------------------------------------
    print("🧾 Extrayendo dígitos numéricos del campo CEDULA...")
    df["cedula"] = df["CEDULA"].apply(extraer_digitos)

    total_inicial = len(df)
    df = df.dropna(subset=["cedula"])
    eliminados = total_inicial - len(df)

    print(f"✔ Cédulas válidas: {len(df)}")
    print(f"🧹 Registros eliminados por cédula inválida: {eliminados}")

    # --------------------------------------------------------
    # Separación nombres / apellidos
    # --------------------------------------------------------
    nombres_apellidos = df["CONTRATISTA"].apply(split_nombres_apellidos)
    df["nombres"] = nombres_apellidos.apply(lambda x: x[0])
    df["apellidos"] = nombres_apellidos.apply(lambda x: x[1])

    df_final = df[["cedula", "nombres", "apellidos"]].copy()
    print(f"📦 Registros preparados para carga: {len(df_final)}")

    # --------------------------------------------------------
    # Inserción en base de datos
    # --------------------------------------------------------
    print("🚀 Iniciando inserción en base de datos...")

    engine = get_engine()

    insert_sql = text("""
        INSERT INTO colaborador_core (cedula, nombres, apellidos)
        VALUES (:cedula, :nombres, :apellidos)
        ON CONFLICT (cedula) DO NOTHING;
    """)

    insertados = 0

    with engine.begin() as conn:
        for _, row in df_final.iterrows():
            result = conn.execute(
                insert_sql,
                {
                    "cedula": row["cedula"],
                    "nombres": row["nombres"],
                    "apellidos": row["apellidos"],
                }
            )
            insertados += result.rowcount

    print("✅ Carga finalizada")
    print(f"📌 Registros nuevos insertados: {insertados}")
    print(f"📌 Registros omitidos (ya existentes): {len(df_final) - insertados}")


# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    main()
