# apps/automatizacion_documental/api.py
import json
import os
import shutil
import subprocess
import uuid
import zipfile
from io import BytesIO
from typing import Any, Dict, Optional, Tuple

from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_GET, require_http_methods

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from apps.accounts.api import _json_ok, _json_error


# -----------------------
# Helpers API-first
# -----------------------
def _require_auth(request):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return _json_error("NOT_AUTHENTICATED", "Not authenticated.", 401)
    return None


def _parse_json(request) -> Tuple[Optional[dict], Optional[str]]:
    try:
        raw = request.body.decode("utf-8-sig")
        return json.loads(raw or "{}"), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _get_session_id(request) -> str:
    if "automatizacion_session" not in request.session:
        request.session["automatizacion_session"] = uuid.uuid4().hex
    return request.session["automatizacion_session"]


def _get_paths(session_id: str) -> Dict[str, str]:
    base = os.path.join(settings.MEDIA_ROOT, "automatizacion", "sesiones", session_id)
    paths = {
        "base": base,
        "original": os.path.join(base, "original"),
        "pdf": os.path.join(base, "pdf"),
        "firmados": os.path.join(base, "firmados"),
    }
    for p in paths.values():
        os.makedirs(p, exist_ok=True)
    return paths


def _count_docx(folder: str) -> int:
    total = 0
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".docx"):
                total += 1
    return total


# -----------------------
# LibreOffice convert
# -----------------------
def _convert_docx_to_pdf(docx_path: str, output_dir: str) -> Tuple[bool, Optional[str]]:
    try:
        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                output_dir,
                docx_path,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True, None
    except subprocess.CalledProcessError as e:
        msg = e.stderr.decode(errors="ignore") if e.stderr else "LibreOffice conversion failed."
        return False, msg
    except Exception as e:
        return False, str(e)


def _sign_pdf(input_pdf: str, firma_png: str, output_pdf: str, firma_cfg: dict) -> None:
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for idx, page in enumerate(reader.pages):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        x = float(firma_cfg["x_ratio"]) * width
        y = float(firma_cfg["y_ratio"]) * height
        w = float(firma_cfg["width_ratio"]) * width
        h = float(firma_cfg["height_ratio"]) * height

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


# -----------------------
# Endpoints
# -----------------------

@require_GET
def health(request):
    err = _require_auth(request)
    if err:
        return err

    session_id = _get_session_id(request)
    paths = _get_paths(session_id)

    firma_png = os.path.join(paths["base"], "firma.png")
    cfg_path = os.path.join(paths["base"], "firma_config.json")
    zip_path = os.path.join(paths["base"], "input.zip")

    return _json_ok(
        {
            "session_id": session_id,
            "paths_ready": True,
            "has_zip": os.path.exists(zip_path),
            "has_signature_image": os.path.exists(firma_png),
            "has_signature_config": os.path.exists(cfg_path),
            "docx_count": _count_docx(paths["original"]),
            "pdf_count": len([f for f in os.listdir(paths["pdf"]) if f.lower().endswith(".pdf")]),
            "signed_pdf_count": len([f for f in os.listdir(paths["firmados"]) if f.lower().endswith(".pdf")]),
        }
    )


@require_http_methods(["POST"])
def upload_zip_firma(request):
    err = _require_auth(request)
    if err:
        return err

    # multipart/form-data
    zip_file = request.FILES.get("zip_file")
    firma_file = request.FILES.get("firma_file")

    if not zip_file or not firma_file:
        return _json_error("VALIDATION_ERROR", "zip_file and firma_file are required.", 400)

    session_id = _get_session_id(request)
    paths = _get_paths(session_id)

    # Limpia carpeta original/pdf/firmados para evitar mezcla con corridas anteriores
    shutil.rmtree(paths["original"], ignore_errors=True)
    shutil.rmtree(paths["pdf"], ignore_errors=True)
    shutil.rmtree(paths["firmados"], ignore_errors=True)
    os.makedirs(paths["original"], exist_ok=True)
    os.makedirs(paths["pdf"], exist_ok=True)
    os.makedirs(paths["firmados"], exist_ok=True)

    zip_path = os.path.join(paths["base"], "input.zip")
    firma_path = os.path.join(paths["base"], "firma.png")

    with open(zip_path, "wb") as f:
        for chunk in zip_file.chunks():
            f.write(chunk)

    with open(firma_path, "wb") as f:
        for chunk in firma_file.chunks():
            f.write(chunk)

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(paths["original"])
    except Exception as e:
        return _json_error("ZIP_EXTRACT_ERROR", str(e), 400)

    total_docx = _count_docx(paths["original"])

    return _json_ok(
        {
            "session_id": session_id,
            "total_docx": total_docx,
        },
        status=201,
    )


@require_GET
def preview_info(request):
    err = _require_auth(request)
    if err:
        return err

    session_id = _get_session_id(request)
    paths = _get_paths(session_id)

    pdfs = sorted([f for f in os.listdir(paths["pdf"]) if f.lower().endswith(".pdf")])

    firma_png = os.path.join(paths["base"], "firma.png")
    cfg_path = os.path.join(paths["base"], "firma_config.json")

    return _json_ok(
        {
            "session_id": session_id,
            "pdfs_generated": pdfs,
            "has_signature_image": os.path.exists(firma_png),
            "has_signature_config": os.path.exists(cfg_path),
            "preview_pdf_endpoint": "/api/automatizacion/preview/pdf/",
            "preview_firma_endpoint": "/api/automatizacion/preview/firma/",
        }
    )


@require_GET
def preview_pdf(request):
    err = _require_auth(request)
    if err:
        return err

    session_id = _get_session_id(request)
    paths = _get_paths(session_id)

    pdfs = sorted([f for f in os.listdir(paths["pdf"]) if f.lower().endswith(".pdf")])
    if not pdfs:
        return _json_error("NO_PDFS", "No PDFs available. Generate PDFs first.", 400)

    pdf_path = os.path.join(paths["pdf"], pdfs[0])
    return FileResponse(open(pdf_path, "rb"), content_type="application/pdf")


@require_GET
def preview_firma(request):
    err = _require_auth(request)
    if err:
        return err

    session_id = _get_session_id(request)
    paths = _get_paths(session_id)

    firma_png = os.path.join(paths["base"], "firma.png")
    if not os.path.exists(firma_png):
        return _json_error("NO_SIGNATURE", "Signature image not uploaded.", 400)

    return FileResponse(open(firma_png, "rb"), content_type="image/png")


@require_http_methods(["POST"])
def save_signature_position(request):
    err = _require_auth(request)
    if err:
        return err

    payload, perr = _parse_json(request)
    if perr:
        return _json_error("INVALID_JSON", f"Invalid JSON body. Detail: {perr}", 400)

    # Requeridos
    required = ["page", "x_ratio", "y_ratio", "width_ratio", "height_ratio"]
    for k in required:
        if k not in payload:
            return _json_error("VALIDATION_ERROR", f"Missing field: {k}", 400)

    try:
        firma_cfg = {
            "page": int(payload.get("page", 1)),
            "x_ratio": float(payload["x_ratio"]),
            "y_ratio": float(payload["y_ratio"]),
            "width_ratio": float(payload["width_ratio"]),
            "height_ratio": float(payload["height_ratio"]),
        }
    except Exception:
        return _json_error("VALIDATION_ERROR", "Invalid numeric values in signature config.", 400)

    session_id = _get_session_id(request)
    paths = _get_paths(session_id)

    cfg_path = os.path.join(paths["base"], "firma_config.json")
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(firma_cfg, f, indent=2)

    return _json_ok({"saved": True, "config": firma_cfg})


@require_http_methods(["POST"])
def generate_signed_pdfs(request):
    err = _require_auth(request)
    if err:
        return err

    session_id = _get_session_id(request)
    paths = _get_paths(session_id)

    firma_png = os.path.join(paths["base"], "firma.png")
    cfg_path = os.path.join(paths["base"], "firma_config.json")

    if not os.path.exists(firma_png):
        return _json_error("MISSING_SIGNATURE", "Upload signature image first.", 400)
    if not os.path.exists(cfg_path):
        return _json_error("MISSING_SIGNATURE_CONFIG", "Save signature position first.", 400)

    with open(cfg_path, "r", encoding="utf-8") as f:
        firma_cfg = json.load(f)

    # 1) Convert docx -> pdf
    conversion_errors = []
    total_docx = 0
    for root, _, files in os.walk(paths["original"]):
        for name in files:
            if name.lower().endswith(".docx"):
                total_docx += 1
                docx_path = os.path.join(root, name)
                ok, msg = _convert_docx_to_pdf(docx_path, paths["pdf"])
                if not ok:
                    conversion_errors.append({"file": name, "error": msg or "convert_failed"})

    # 2) Sign pdfs
    sign_errors = []
    signed = 0
    for name in os.listdir(paths["pdf"]):
        if name.lower().endswith(".pdf"):
            try:
                _sign_pdf(
                    input_pdf=os.path.join(paths["pdf"], name),
                    firma_png=firma_png,
                    output_pdf=os.path.join(paths["firmados"], name),
                    firma_cfg=firma_cfg,
                )
                signed += 1
            except Exception as e:
                sign_errors.append({"file": name, "error": str(e)})

    return _json_ok(
        {
            "total_docx_found": total_docx,
            "pdf_generated": len([f for f in os.listdir(paths["pdf"]) if f.lower().endswith(".pdf")]),
            "pdf_signed": signed,
            "conversion_errors": conversion_errors,
            "sign_errors": sign_errors,
        }
    )


@require_GET
def download_zip(request):
    err = _require_auth(request)
    if err:
        return err

    session_id = _get_session_id(request)
    paths = _get_paths(session_id)

    firmados = [f for f in os.listdir(paths["firmados"]) if f.lower().endswith(".pdf")]
    if not firmados:
        return _json_error("NO_SIGNED_PDFS", "No signed PDFs available. Run generate first.", 400)

    zip_name = f"pdf_firmados_{session_id}.zip"
    zip_path = os.path.join(paths["base"], zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in firmados:
            z.write(os.path.join(paths["firmados"], f), arcname=f)

    return FileResponse(open(zip_path, "rb"), as_attachment=True, filename=zip_name)
