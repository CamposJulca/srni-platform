    # import zipfile
    # import uuid
    # from pathlib import Path
    # from django.conf import settings


    # def procesar_zip_documentos(zip_file):
    #     """
    #     Guarda el ZIP recibido, valida su contenido y extrae documentos .docx
    #     en una carpeta de sesión aislada.

    #     Estructura resultante:
    #     media/
    #     automatizacion/
    #         sesiones/
    #         <session_id>/
    #             input.zip
    #             original/
    #             *.docx
    #     """

    #     print(">>> procesar_zip_documentos EJECUTADO <<<")

    #     # =========================
    #     # 1. Crear sesión única
    #     # =========================
    #     session_id = uuid.uuid4().hex
    #     print(f">>> Session ID: {session_id}")

    #     # =========================
    #     # 2. Definir rutas
    #     # =========================
    #     base_path = (
    #         Path(settings.MEDIA_ROOT)
    #         / "automatizacion"
    #         / "sesiones"
    #         / session_id
    #     )

    #     original_path = base_path / "original"
    #     original_path.mkdir(parents=True, exist_ok=True)

    #     zip_path = base_path / "input.zip"

    #     print(f">>> Ruta base: {base_path}")
    #     print(f">>> Ruta original: {original_path}")

    #     # =========================
    #     # 3. Guardar ZIP en disco
    #     # =========================
    #     with open(zip_path, "wb") as destination:
    #         for chunk in zip_file.chunks():
    #             destination.write(chunk)

    #     print(f">>> ZIP guardado en: {zip_path}")

    #     # =========================
    #     # 4. Validar y extraer ZIP
    #     # =========================
    #     with zipfile.ZipFile(zip_path, "r") as zip_ref:
    #         nombres = zip_ref.namelist()

    #         print(">>> Contenido del ZIP:")
    #         for n in nombres:
    #             print("   -", n)

    #         if not nombres:
    #             raise ValueError("El ZIP está vacío")

    #         archivos_docx = []

    #         for file in nombres:
    #             # Ignorar carpetas
    #             if file.endswith("/"):
    #                 continue

    #             # Validar extensión
    #             if not file.lower().endswith(".docx"):
    #                 raise ValueError(
    #                     f"Archivo no permitido en el ZIP: {file}"
    #                 )

    #             archivos_docx.append(file)

    #         if not archivos_docx:
    #             raise ValueError(
    #                 "El ZIP no contiene archivos .docx válidos"
    #             )

    #         # Extraer TODO (mantiene estructura interna si existe)
    #         zip_ref.extractall(original_path)

    #     # =========================
    #     # 5. Contar archivos extraídos
    #     # =========================
    #     total_archivos = len(
    #         list(original_path.rglob("*.docx"))
    #     )

    #     if total_archivos == 0:
    #         raise ValueError(
    #             "No se encontraron archivos .docx después de la extracción"
    #         )

    #     print(f">>> ZIP procesado correctamente: {total_archivos} archivos DOCX <<<")

    #     # =========================
    #     # 6. Retornar metadata
    #     # =========================
    #     return {
    #         "session_id": session_id,
    #         "ruta_original": str(original_path),
    #         "total_archivos": total_archivos,
    #     }


import zipfile
import uuid
from pathlib import Path
from django.conf import settings
from .log_service import write_log


def procesar_zip_documentos(zip_file):
    session_id = uuid.uuid4().hex

    base_path = (
        Path(settings.MEDIA_ROOT)
        / "automatizacion"
        / "sesiones"
        / session_id
    )

    original_path = base_path / "original"
    original_path.mkdir(parents=True, exist_ok=True)

    zip_path = base_path / "input.zip"

    write_log(base_path, f"📦 Creando sesión {session_id}")
    write_log(base_path, "📥 Guardando ZIP recibido")

    with open(zip_path, "wb") as destination:
        for chunk in zip_file.chunks():
            destination.write(chunk)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        archivos_docx = [
            f for f in zip_ref.namelist()
            if f.lower().endswith(".docx") and not f.endswith("/")
        ]

        if not archivos_docx:
            raise ValueError("El ZIP no contiene archivos .docx")

        zip_ref.extractall(original_path)

    total = len(list(original_path.rglob("*.docx")))
    write_log(base_path, f"✅ ZIP procesado correctamente ({total} documentos)")

    return {
        "session_id": session_id,
        "total_archivos": total,
    }
