import pandas as pd
import psycopg2
from pathlib import Path

print("\n==============================")
print("INICIO VALIDACIÓN DE CÉDULAS")
print("==============================\n")

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

print(f"[INFO] Ruta del Excel: {EXCEL_PATH.resolve()}")

# -----------------------------------
# 1. LEER EXCEL
# -----------------------------------
print("\n[STEP 1] Leyendo archivo Excel...")
df = pd.read_excel(EXCEL_PATH, sheet_name=0)
print(f"[OK] Excel cargado correctamente")
print(f"[INFO] Total filas leídas: {len(df)}")
print(f"[INFO] Columnas detectadas: {list(df.columns)}")

# -----------------------------------
# 2. LIMPIEZA Y NORMALIZACIÓN DE CÉDULAS
# -----------------------------------
print("\n[STEP 2] Normalizando columna 'NUMERO DE CEDULA'...")

if "NUMERO DE CEDULA" not in df.columns:
    raise ValueError("❌ La columna 'NUMERO DE CEDULA' no existe en el Excel")

print("[INFO] Eliminando valores nulos de cédula...")
df_cedulas = df[["NUMERO DE CEDULA"]].dropna()
print(f"[INFO] Filas con cédula válida: {len(df_cedulas)}")

print("[INFO] Convirtiendo cédulas a string...")
df_cedulas["NUMERO DE CEDULA"] = (
    df_cedulas["NUMERO DE CEDULA"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.strip()
)

cedulas_excel = set(df_cedulas["NUMERO DE CEDULA"].unique())

print(f"[OK] Cédulas únicas encontradas en Excel: {len(cedulas_excel)}")

# Mostrar muestra
print("[DEBUG] Ejemplo de cédulas Excel:", list(cedulas_excel)[:5])

# -----------------------------------
# 3. CONEXIÓN A BASE DE DATOS
# -----------------------------------
print("\n[STEP 3] Conectando a la base de datos PostgreSQL...")

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

print("[OK] Conexión exitosa a PostgreSQL")

# -----------------------------------
# 4. LECTURA DE CÉDULAS DESDE BD
# -----------------------------------
print("\n[STEP 4] Consultando cédulas en tabla 'colaborador'...")

cur.execute("SELECT cedula FROM colaborador;")
rows = cur.fetchall()

print(f"[INFO] Registros obtenidos desde BD: {len(rows)}")

cedulas_bd = {row[0].strip() for row in rows if row[0]}

print(f"[OK] Cédulas únicas en BD: {len(cedulas_bd)}")
print("[DEBUG] Ejemplo de cédulas BD:", list(cedulas_bd)[:5])

cur.close()
conn.close()

print("[OK] Conexión cerrada")

# -----------------------------------
# 5. COMPARACIÓN DE CONJUNTOS
# -----------------------------------
print("\n[STEP 5] Comparando cédulas Excel vs Base de Datos...")

solo_en_excel = sorted(cedulas_excel - cedulas_bd)
solo_en_bd = sorted(cedulas_bd - cedulas_excel)
coinciden = sorted(cedulas_excel & cedulas_bd)

print("\n[RESULTADOS]")
print(f"✔ Coinciden (Excel ∩ BD): {len(coinciden)}")
print(f"➕ Solo en Excel (faltan en BD): {len(solo_en_excel)}")
print(f"➖ Solo en BD (no vienen en Excel): {len(solo_en_bd)}")

print("\n[DEBUG] Ejemplo COINCIDEN:", coinciden[:5])
print("[DEBUG] Ejemplo SOLO_EN_EXCEL:", solo_en_excel[:5])
print("[DEBUG] Ejemplo SOLO_EN_BD:", solo_en_bd[:5])

# -----------------------------------
# 6. EXPORTAR RESULTADOS
# -----------------------------------
print("\n[STEP 6] Exportando resultados a Excel...")

output_path = Path("../data/validacion_cedulas_04122025.xlsx")

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    pd.DataFrame({"cedula": coinciden}).to_excel(
        writer, sheet_name="COINCIDEN", index=False
    )
    print("[OK] Hoja COINCIDEN exportada")

    pd.DataFrame({"cedula": solo_en_excel}).to_excel(
        writer, sheet_name="SOLO_EN_EXCEL", index=False
    )
    print("[OK] Hoja SOLO_EN_EXCEL exportada")

    pd.DataFrame({"cedula": solo_en_bd}).to_excel(
        writer, sheet_name="SOLO_EN_BD", index=False
    )
    print("[OK] Hoja SOLO_EN_BD exportada")

print(f"\n[FIN] Archivo generado exitosamente:")
print(f"     {output_path.resolve()}")

print("\n==============================")
print("FIN VALIDACIÓN DE CÉDULAS")
print("==============================\n")
