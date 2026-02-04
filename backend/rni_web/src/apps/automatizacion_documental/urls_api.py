# apps/automatizacion_documental/urls_api.py
from django.urls import path
from . import api

urlpatterns = [
    path("automatizacion/health/", api.health, name="api_automatizacion_health"),
    path("automatizacion/upload/", api.upload_zip_firma, name="api_automatizacion_upload"),
    path("automatizacion/preview/", api.preview_info, name="api_automatizacion_preview_info"),
    path("automatizacion/preview/pdf/", api.preview_pdf, name="api_automatizacion_preview_pdf"),
    path("automatizacion/preview/firma/", api.preview_firma, name="api_automatizacion_preview_firma"),
    path("automatizacion/firma/position/", api.save_signature_position, name="api_automatizacion_save_signature_position"),
    path("automatizacion/generate/", api.generate_signed_pdfs, name="api_automatizacion_generate"),
    path("automatizacion/download/", api.download_zip, name="api_automatizacion_download"),
    path("automatizacion/preview/convert/", api.preview_convert, name="api_automatizacion_preview_convert"),

]
