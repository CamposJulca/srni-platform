from docx import Document
from docx.shared import Cm
from pathlib import Path


def cambiar_a_oficio(docx_path: Path):
    """
    Cambia el tamaño de la página a OFICIO/FOLIO
    sin alterar el contenido del documento.
    """

    doc = Document(docx_path)
    section = doc.sections[0]

    # Tamaño OFICIO / FOLIO
    section.page_width = Cm(21.59)    # ancho carta
    section.page_height = Cm(33.02)   # alto oficio

    # Márgenes estándar institucionales
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

    doc.save(docx_path)
