import pandas as pd
import psycopg2
from pathlib import Path

print("\n==============================================")
print("INICIO INSERCIÓN NUEVOS CONTRATISTAS (BÁSICO)")
print("==============================================\n")

# -----------------------------------
# CONFIGURACIÓN
# -----------------------------------
EXCEL_PATH = Path("../data/04122025 ID Contratación 2026.xlsx")

DB_CONFIG = {
    "host": "localhost",
    "dbname": "srni_actividades",
    "user": "postgres",
    "password": "Alejito10."
}

print(f"[INFO] Excel origen: {EXCEL_PATH.resolve()}")

# -----------------------------------
# 1. LEER EXCEL
# -----------------------------------
print("\n[STEP 1] Leyendo Excel...")
df = pd.read_excel(EXCEL_PATH, sheet_name=0)

print(f"[OK] Filas totales leídas: {len(df)}")

# -----------------------------------
# 2. NORMALIZAR DATOS BÁSICOS
# -----------------------------------
print("\n[STEP 2] Normalizando columnas necesarias...")

required_cols = [
    "NUMERO DE CEDULA",
    "NOMBRES CONTRATISTA",
    "APELLIDOS CONTRATISTA"
]

for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Falta la columna obligatoria: {col}")

df = df[required_cols].dropna(subset=["NUMERO DE CEDULA"])

print(f"[INFO] Filas con cédula válida: {len(df)}")

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

df = df[["cedula", "nombre"]].drop_duplicates(subset=["cedula"])

print(f"[OK] Cédulas únicas en Excel: {len(df)}")
print("[DEBUG] Ejemplo registros a evaluar:")
print(df.head())

# -----------------------------------
# 3. CONECTAR A BD Y OBTENER CÉDULAS EXISTENTES
# -----------------------------------
print("\n[STEP 3] Conectando a PostgreSQL...")

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

print("[OK] Conexión establecida")

cur.execute("SELECT cedula FROM colaborador;")
cedulas_bd = {row[0] for row in cur.fetchall()}

print(f"[INFO] Cédulas existentes en BD: {len(cedulas_bd)}")

# -----------------------------------
# 4. FILTRAR SOLO NUEVOS CONTRATISTAS
# -----------------------------------
print("\n[STEP 4] Filtrando nuevos contratistas (NO existentes en BD)...")

df_nuevos = df[~df["cedula"].isin(cedulas_bd)]

print(f"[RESULTADO] Nuevos contratistas a insertar: {len(df_nuevos)}")

if df_nuevos.empty:
    print("⚠️ No hay nuevos registros para insertar.")
    cur.close()
    conn.close()
    exit(0)

print("[DEBUG] Ejemplo de nuevos contratistas:")
print(df_nuevos.head())

# -----------------------------------
# 5. INSERCIÓN CONTROLADA
# -----------------------------------
print("\n[STEP 5] Insertando registros en tabla 'colaborador'...")

insert_sql = """
INSERT INTO colaborador (cedula, nombre, tipo_vinculacion, estado)
VALUES (%s, %s, %s, %s)
"""

insertados = 0
errores = 0

for _, row in df_nuevos.iterrows():
    try:
        print(f"[INSERT] Cédula={row['cedula']} | Nombre='{row['nombre']}'")
        cur.execute(
            insert_sql,
            (row["cedula"], row["nombre"], "Contrato", "Activo")
        )
        insertados += 1
    except Exception as e:
        print(f"❌ ERROR al insertar cédula {row['cedula']}: {e}")
        errores += 1

conn.commit()

print("\n[COMMIT] Transacción confirmada")

cur.close()
conn.close()

# -----------------------------------
# 6. RESUMEN FINAL
# -----------------------------------
print("\n==============================================")
print("RESUMEN INSERCIÓN")
print("==============================================")
print(f"✔ Insertados correctamente: {insertados}")
print(f"❌ Errores: {errores}")
print("==============================================\n")
print("FIN DEL PROCESO\n")
