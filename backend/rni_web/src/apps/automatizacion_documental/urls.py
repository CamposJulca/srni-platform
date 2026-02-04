# apps/automatizacion_documental/urls.py
from django.urls import path
from . import api

urlpatterns = [
    path("health/", api.health),
    path("upload/", api.upload_zip_firma),

    # ✅ NUEVO (Enfoque B)
    path("preview/convert/", api.preview_convert),

    path("preview/", api.preview_info),
    path("preview/pdf/", api.preview_pdf),
    path("preview/firma/", api.preview_firma),

    path("firma/position/", api.save_signature_position),
    path("generate/", api.generate_signed_pdfs),
    path("download/", api.download_zip),
]
