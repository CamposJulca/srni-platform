import os
import uuid
import json
import zipfile
import subprocess
import shutil
from io import BytesIO

from django.conf import settings
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


# ======================================================
# VISTA PRINCIPAL
# ======================================================

def documentos_view(request):
    print("[VIEW] documentos_view")
    return render(request, "automatizacion/documentos.html")


# ======================================================
# SESIÓN Y DIRECTORIOS
# ======================================================

def get_session_id(request):
    if "automatizacion_session" not in request.session:
        request.session["automatizacion_session"] = uuid.uuid4().hex
        print("[SESSION] Nueva sesión:", request.session["automatizacion_session"])
    else:
        print("[SESSION] Sesión existente:", request.session["automatizacion_session"])
    return request.session["automatizacion_session"]


def get_paths(session_id):
    base = os.path.join(
        settings.MEDIA_ROOT,
        "automatizacion",
        "sesiones",
        session_id
    )

    paths = {
        "base": base,
        "original": os.path.join(base, "original"),
        "pdf": os.path.join(base, "pdf"),
        "firmados": os.path.join(base, "firmados"),
    }

    for k, p in paths.items():
        os.makedirs(p, exist_ok=True)
        print(f"[PATH {k}]", p)

    return paths


# ======================================================
# PASO 1 — CARGAR ZIP + FIRMA
# ======================================================

@csrf_exempt
def cargar_zip(request):
    print("\n[VIEW] cargar_zip")

    session_id = get_session_id(request)
    paths = get_paths(session_id)

    zip_file = request.FILES.get("zip_file")
    firma_file = request.FILES.get("firma_file")

    print("[FILES]", zip_file, firma_file)

    if not zip_file or not firma_file:
        return JsonResponse({"error": "ZIP y firma son obligatorios"}, status=400)

    zip_path = os.path.join(paths["base"], "input.zip")
    firma_path = os.path.join(paths["base"], "firma.png")

    with open(zip_path, "wb") as f:
        for chunk in zip_file.chunks():
            f.write(chunk)

    with open(firma_path, "wb") as f:
        for chunk in firma_file.chunks():
            f.write(chunk)

    print("[GUARDADO] ZIP y firma")

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(paths["original"])

    total = sum(
        1
        for root, _, files in os.walk(paths["original"])
        for f in files
        if f.lower().endswith(".docx")
    )

    print("[DOCX ENCONTRADOS]", total)

    return JsonResponse({"total_archivos": total})


# ======================================================
# PASO INTERMEDIO — POSICIONAR FIRMA (PREVIEW)
# ======================================================

def posicionar_firma_view(request):
    print("\n[VIEW] posicionar_firma_view")

    session_id = get_session_id(request)
    paths = get_paths(session_id)

    preview_dir = os.path.join(
        settings.MEDIA_ROOT,
        "automatizacion",
        "preview"
    )
    os.makedirs(preview_dir, exist_ok=True)
    print("[PREVIEW DIR]", preview_dir)

    pdfs = [
        f for f in os.listdir(paths["pdf"])
        if f.lower().endswith(".pdf")
    ]

    print("[PDFS DISPONIBLES]", pdfs)

    if not pdfs:
        return JsonResponse(
            {"error": "No hay PDFs generados para previsualizar"},
            status=400
        )

    shutil.copy(
        os.path.join(paths["pdf"], pdfs[0]),
        os.path.join(preview_dir, "documento.pdf")
    )

    shutil.copy(
        os.path.join(paths["base"], "firma.png"),
        os.path.join(preview_dir, "firma.png")
    )

    print("[PREVIEW OK]")

    return render(request, "automatizacion/posicionar_firma.html")


# ======================================================
# PASO 2 — GUARDAR POSICIÓN DE FIRMA
# ======================================================

@csrf_exempt
def guardar_posicion_firma(request):
    print("\n[VIEW] guardar_posicion_firma")

    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        print("[DATA]", data)

        session_id = get_session_id(request)
        paths = get_paths(session_id)

        firma_cfg = {
            "page": int(data.get("page", 1)),
            "x_ratio": float(data["x_ratio"]),
            "y_ratio": float(data["y_ratio"]),
            "width_ratio": float(data["width_ratio"]),
            "height_ratio": float(data["height_ratio"]),
        }

        cfg_path = os.path.join(paths["base"], "firma_config.json")

        with open(cfg_path, "w") as f:
            json.dump(firma_cfg, f, indent=4)

        print("[CFG GUARDADA]", firma_cfg)

        return JsonResponse({"ok": True})

    except Exception as e:
        print("[ERROR GUARDAR CFG]", str(e))
        return JsonResponse({"error": str(e)}, status=400)


# ======================================================
# CONVERSIÓN DOCX → PDF
# ======================================================

def convertir_docx_a_pdf(docx_path, output_dir):
    print("[CONVERTIR DOCX]")
    print("  DOCX:", docx_path)

    try:
        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", output_dir,
                docx_path,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("[OK] DOCX → PDF")
        return True

    except subprocess.CalledProcessError as e:
        print("[ERROR LIBREOFFICE]")
        print(e.stderr.decode(errors="ignore"))
        return False


# ======================================================
# FIRMA PDF
# ======================================================

def firmar_pdf(input_pdf, firma_png, output_pdf, firma_cfg):
    print("[FIRMAR PDF]", input_pdf)

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for idx, page in enumerate(reader.pages):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        x = firma_cfg["x_ratio"] * width
        y = firma_cfg["y_ratio"] * height
        w = firma_cfg["width_ratio"] * width
        h = firma_cfg["height_ratio"] * height

        print(f"  [PAGE {idx+1}] x={x} y={y} w={w} h={h}")

        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=(width, height))

        can.drawImage(
            ImageReader(firma_png),
            x=x,
            y=y,
            width=w,
            height=h,
            mask="auto",
        )

        can.save()
        packet.seek(0)

        overlay = PdfReader(packet).pages[0]
        page.merge_page(overlay)
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print("[PDF FIRMADO OK]", output_pdf)


# ======================================================
# PASO 3 — GENERAR Y FIRMAR PDFs
# ======================================================

@csrf_exempt
def generar_pdfs(request):
    print("\n[VIEW] generar_pdfs")

    session_id = get_session_id(request)
    paths = get_paths(session_id)

    firma_png = os.path.join(paths["base"], "firma.png")
    cfg_path = os.path.join(paths["base"], "firma_config.json")

    if not os.path.exists(firma_png) or not os.path.exists(cfg_path):
        return JsonResponse({"error": "Faltan insumos"}, status=400)

    with open(cfg_path) as f:
        firma_cfg = json.load(f)

    errores = []
    total = 0

    for root, _, files in os.walk(paths["original"]):
        for f in files:
            if f.lower().endswith(".docx"):
                ok = convertir_docx_a_pdf(
                    os.path.join(root, f),
                    paths["pdf"]
                )
                if not ok:
                    errores.append(f)

    for f in os.listdir(paths["pdf"]):
        if f.lower().endswith(".pdf"):
            try:
                firmar_pdf(
                    os.path.join(paths["pdf"], f),
                    firma_png,
                    os.path.join(paths["firmados"], f),
                    firma_cfg
                )
                total += 1
            except Exception as e:
                print("[ERROR FIRMANDO]", f, str(e))
                errores.append(f)

    print("[RESULTADO] FIRMADOS:", total)
    print("[ERRORES]", errores)

    return JsonResponse({
        "total_pdfs": total,
        "errores": errores
    })


# ======================================================
# PASO 4 — DESCARGAR ZIP FINAL
# ======================================================

def descargar_zip(request):
    print("\n[VIEW] descargar_zip")

    session_id = get_session_id(request)
    base = os.path.join(
        settings.MEDIA_ROOT,
        "automatizacion",
        "sesiones",
        session_id
    )

    zip_name = f"pdf_firmados_{session_id}.zip"
    zip_path = os.path.join(base, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        firmados_dir = os.path.join(base, "firmados")
        for f in os.listdir(firmados_dir):
            z.write(os.path.join(firmados_dir, f), arcname=f)

    print("[ZIP GENERADO]", zip_name)

    return FileResponse(
        open(zip_path, "rb"),
        as_attachment=True,
        filename=zip_name,
    )