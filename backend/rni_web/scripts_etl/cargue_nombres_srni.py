import pandas as pd

EXCEL_PATH = "../data/SUBDIRECCION RED NACIONAL DE INFORMACION MATRIZ.xlsx"

print("="*60)
print("CARGA Y NORMALIZACIÓN MATRIZ FINAL RNI")
print("="*60)

df = pd.read_excel(EXCEL_PATH)

print(f"[INFO] Filas originales: {len(df)}")

df = df[
    ["ID 2026", "NUMERO DE CEDULA", "NOMBRES CONTRATISTA", "APELLIDOS CONTRATISTA"]
]

# Normalización
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

print(f"[INFO] Registros normalizados únicos: {len(df)}")
print("[DEBUG] Ejemplo:")
print(df.head(10))
