# apps/colaboradores/admin.py
from django.contrib import admin
from .models import ColaboradorCore

@admin.register(ColaboradorCore)
class ColaboradorCoreAdmin(admin.ModelAdmin):
    list_display = ("id", "cedula", "nombres", "apellidos", "estado", "fecha_creacion")
    search_fields = ("cedula", "nombres", "apellidos")
    list_filter = ("estado",)