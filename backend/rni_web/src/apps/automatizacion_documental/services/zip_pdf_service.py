import zipfile
from pathlib import Path


def crear_zip_pdfs(pdf_path: Path, zip_destino: Path):
    """
    Crea un ZIP con todos los PDFs generados.
    """
    with zipfile.ZipFile(zip_destino, "w", zipfile.ZIP_DEFLATED) as zipf:
        for pdf in pdf_path.glob("*.pdf"):
            zipf.write(pdf, arcname=pdf.name)
