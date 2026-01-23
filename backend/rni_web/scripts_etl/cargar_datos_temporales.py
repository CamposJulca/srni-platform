import pandas as pd
import psycopg2
from pathlib import Path

print("\n======================================")
print("CARGA STAGING: NOMBRES DESDE EXCEL")
print("======================================\n")

EXCEL_PATH = Path("../data/04122025 ID Contratación 2026.xlsx")

DB_CONFIG = {
    "host": "localhost",
    "dbname": "srni_actividades",
    "user": "postgres",
    "password": "Alejito10."
}

# -----------------------------------
# 1. LEER EXCEL
# -----------------------------------
print("[STEP 1] Leyendo Excel...")

df = pd.read_excel(EXCEL_PATH, sheet_name=0)

df = df[
    ["NUMERO DE CEDULA", "NOMBRES CONTRATISTA", "APELLIDOS CONTRATISTA"]
].dropna(subset=["NUMERO DE CEDULA"])

df["cedula"] = (
    df["NUMERO DE CEDULA"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.strip()
)

df["nombre"] = (
    df["NOMBRES CONTRATISTA"].fillna("").str.strip()
    + " "
    + df["APELLIDOS CONTRATISTA"].fillna("").str.strip()
).str.strip()

df = df[["cedula", "nombre"]].drop_duplicates()

print(f"[INFO] Registros únicos a cargar: {len(df)}")

# -----------------------------------
# 2. CONEXIÓN BD
# -----------------------------------
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

print("[OK] Conexión establecida")

# -----------------------------------
# 3. LIMPIAR STAGING
# -----------------------------------
print("[STEP 2] Limpiando tabla staging...")

cur.execute("TRUNCATE TABLE staging_excel_nombres;")

# -----------------------------------
# 4. INSERTAR STAGING
# -----------------------------------
print("[STEP 3] Insertando registros en staging...")

for _, r in df.iterrows():
    cur.execute(
        "INSERT INTO staging_excel_nombres (cedula, nombre) VALUES (%s, %s)",
        (r["cedula"], r["nombre"])
    )

conn.commit()

print("[OK] Datos cargados en staging")

cur.close()
conn.close()

print("\n✔ STAGING LISTO PARA CONSULTAS\n")
