import pandas as pd
import psycopg2
from pathlib import Path

print("\n======================================================")
print("CARGA STAGING EXCEL → CODIGO_2026 (POSTGRESQL)")
print("======================================================\n")

# ------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------
EXCEL_PATH = Path("../data/04122025 ID Contratación 2026.xlsx")

DB_CONFIG = {
    "host": "localhost",
    "dbname": "srni_actividades",
    "user": "postgres",
    "password": "Alejito10."   # <-- AJUSTA ESTO
}

# ------------------------------------------------------
# STEP 1. LEER EXCEL
# ------------------------------------------------------
print("[STEP 1] Leyendo archivo Excel...")

df = pd.read_excel(EXCEL_PATH, sheet_name=0)

print(f"[INFO] Filas totales leídas: {len(df)}")

# ------------------------------------------------------
# STEP 2. SELECCIÓN DE COLUMNAS CLAVE
# ------------------------------------------------------
print("[STEP 2] Seleccionando columnas necesarias...")

df = df[
    ["ID 2026", "NUMERO DE CEDULA", "NOMBRES CONTRATISTA", "APELLIDOS CONTRATISTA"]
]

# ------------------------------------------------------
# STEP 3. LIMPIEZA Y NORMALIZACIÓN
# ------------------------------------------------------
print("[STEP 3] Normalizando cédula, nombre y código 2026...")

# Cédula (puede venir nula)
df["cedula"] = (
    df["NUMERO DE CEDULA"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.strip()
)

df.loc[df["cedula"].isin(["nan", "None", ""]), "cedula"] = None

# Código administrativo
df["codigo_2026"] = df["ID 2026"].astype(int)

# Nombre completo
df["nombre"] = (
    df["NOMBRES CONTRATISTA"].fillna("").str.strip()
    + " "
    + df["APELLIDOS CONTRATISTA"].fillna("").str.strip()
).str.strip()

# Dataset final
df = df[["cedula", "nombre", "codigo_2026"]].drop_duplicates()

print(f"[INFO] Registros únicos preparados: {len(df)}")
print("[DEBUG] Ejemplo de registros:")
print(df.head())

# ------------------------------------------------------
# STEP 4. CONEXIÓN A POSTGRESQL
# ------------------------------------------------------
print("\n[STEP 4] Conectando a PostgreSQL...")

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

print("[OK] Conexión establecida")

# ------------------------------------------------------
# STEP 5. LIMPIAR STAGING
# ------------------------------------------------------
print("\n[STEP 5] Limpiando tabla staging_excel_nombres...")

cur.execute("TRUNCATE TABLE staging_excel_nombres;")

# ------------------------------------------------------
# STEP 6. INSERTAR EN STAGING
# ------------------------------------------------------
print("\n[STEP 6] Insertando registros en staging...")

insertados = 0

for _, row in df.iterrows():
    cur.execute(
        """
        INSERT INTO staging_excel_nombres (cedula, nombre, codigo_2026)
        VALUES (%s, %s, %s)
        """,
        (row["cedula"], row["nombre"], row["codigo_2026"])
    )

    print(
        f"[INSERT] codigo_2026={row['codigo_2026']} | "
        f"cedula={row['cedula']} | nombre='{row['nombre']}'"
    )

    insertados += 1

conn.commit()

print("\n[COMMIT] Inserción confirmada")

# ------------------------------------------------------
# STEP 7. CIERRE
# ------------------------------------------------------
cur.close()
conn.close()

print("\n======================================================")
print("RESUMEN CARGA STAGING")
print("======================================================")
print(f"✔ Registros insertados en staging: {insertados}")
print("======================================================")
print("\nFIN DEL PROCESO\n")
