import subprocess
from pathlib import Path

def convertir_docx_a_pdf(docx_path: Path, output_dir: Path):
    output_dir.mkdir(exist_ok=True)

    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            str(docx_path),
            "--outdir",
            str(output_dir),
        ],
        check=True
    )
