# import subprocess
# from pathlib import Path


# def convertir_docx_a_pdf(docx_path: Path, output_dir: Path):
#     """
#     Convierte un archivo DOCX a PDF usando LibreOffice headless.
#     """
#     output_dir.mkdir(exist_ok=True)

#     command = [
#         "libreoffice",
#         "--headless",
#         "--convert-to", "pdf",
#         "--outdir", str(output_dir),
#         str(docx_path)
#     ]

#     result = subprocess.run(
#         command,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )

#     if result.returncode != 0:
#         raise RuntimeError(result.stderr)

import subprocess
from pathlib import Path


# def convertir_docx_a_pdf(docx_path: Path, output_dir: Path):
#     output_dir.mkdir(exist_ok=True)

#     command = [
#         "libreoffice",
#         "--headless",
#         "--convert-to", "pdf",
#         "--outdir", str(output_dir),
#         str(docx_path)
#     ]

#     result = subprocess.run(
#         command,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )

#     if result.returncode != 0:
#         raise RuntimeError(result.stderr)

import subprocess
from pathlib import Path


def convertir_docx_a_pdf(docx_path: Path, output_dir: Path):
    output_dir.mkdir(exist_ok=True)

    command = [
        "libreoffice",
        "--headless",
        "--nologo",
        "--nofirststartwizard",
        "--nodefault",
        "--nolockcheck",
        "--norestore",
        "--convert-to", "pdf:writer_pdf_Export",
        "--outdir", str(output_dir),
        str(docx_path)
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)
