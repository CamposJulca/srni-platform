import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch

EXCEL_PATH = "../data/SUBDIRECCION RED NACIONAL DE INFORMACION MATRIZ.xlsx"

print("=" * 70)
print("CARGA STAGING SRNI 2026")
print("=" * 70)

# ------------------------------------------------------------------
# 1. Leer Excel
# ------------------------------------------------------------------
print("[STEP 1] Leyendo archivo Excel...")
df = pd.read_excel(EXCEL_PATH)
print(f"[OK] Filas originales leídas: {len(df)}")

# ------------------------------------------------------------------
# 2. Seleccionar columnas relevantes
# ------------------------------------------------------------------
print("[STEP 2] Seleccionando columnas relevantes...")
df = df[
    ["ID 2026", "NUMERO DE CEDULA", "NOMBRES CONTRATISTA", "APELLIDOS CONTRATISTA"]
]
print("[OK] Columnas seleccionadas")

# ------------------------------------------------------------------
# 3. Normalización
# ------------------------------------------------------------------
print("[STEP 3] Normalizando datos...")

df["cedula"] = (
    df["NUMERO DE CEDULA"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.strip()
)

df.loc[df["cedula"].isin(["nan", "None", ""]), "cedula"] = None

df["codigo_2026"] = pd.to_numeric(df["ID 2026"], errors="coerce")

df["nombre"] = (
    df["NOMBRES CONTRATISTA"].fillna("").str.strip()
    + " "
    + df["APELLIDOS CONTRATISTA"].fillna("").str.strip()
).str.upper().str.strip()

df = df[["codigo_2026", "cedula", "nombre"]].drop_duplicates()

# ------------------------------------------------------------------
# 4. Filtrar registros válidos
# ------------------------------------------------------------------
df = df[df["codigo_2026"].notna()]
df["codigo_2026"] = df["codigo_2026"].astype(int)

print(f"[OK] Registros válidos a insertar: {len(df)}")
print("[DEBUG] Ejemplo:")
print(df.head(10))

# ------------------------------------------------------------------
# 5. Conexión a PostgreSQL
# ------------------------------------------------------------------
print("[STEP 4] Conectando a PostgreSQL...")
conn = psycopg2.connect(
    dbname="srni_actividades",
    user="postgres",
    password="Alejito10.",  # ajusta si aplica
    host="localhost",
    port=5432
)
cur = conn.cursor()
print("[OK] Conexión establecida")

# ------------------------------------------------------------------
# 6. Insertar en staging
# ------------------------------------------------------------------
print("[STEP 5] Insertando datos en staging_srni_2026...")

insert_sql = """
INSERT INTO staging_srni_2026 (codigo_2026, cedula, nombre)
VALUES (%s, %s, %s)
"""

records = df.values.tolist()
execute_batch(cur, insert_sql, records, page_size=100)

conn.commit()
cur.close()
conn.close()

print("[OK] Inserción completada correctamente")
print("=" * 70)
print("FIN DEL PROCESO")
print("=" * 70)
