from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
import io

def firmar_pdf(pdf_path, firma_img_path, x=350, y=50, w=150, h=60):
    packet = io.BytesIO()

    can = canvas.Canvas(packet, pagesize=letter)
    can.drawImage(
        str(firma_img_path),
        x, y,
        width=w,
        height=h,
        mask='auto'
    )
    can.save()

    packet.seek(0)
    firma_pdf = PdfReader(packet)
    original_pdf = PdfReader(str(pdf_path))

    writer = PdfWriter()

    for i, page in enumerate(original_pdf.pages):
        if i == len(original_pdf.pages) - 1:
            page.merge_page(firma_pdf.pages[0])
        writer.add_page(page)

    with open(pdf_path, "wb") as f:
        writer.write(f)
