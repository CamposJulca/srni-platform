from django.urls import path
from . import views

app_name = "automatizacion"

urlpatterns = [
    path("", views.documentos_view, name="documentos"),

    path("cargar-zip/", views.cargar_zip, name="cargar_zip"),

    path(
        "posicionar-firma/",
        views.posicionar_firma_view,
        name="posicionar_firma",
    ),

    path(
        "guardar-posicion-firma/",
        views.guardar_posicion_firma,
        name="guardar_posicion_firma",
    ),

    path("generar-pdfs/", views.generar_pdfs, name="generar_pdfs"),
    path("descargar-zip/", views.descargar_zip, name="descargar_zip"),
]
