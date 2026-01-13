from django.contrib import admin
from .models import ColaboradorCore, ContratoCore, ColaboradorContrato

@admin.register(ColaboradorCore)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ("cedula", "nombres", "apellidos", "estado")
    search_fields = ("cedula", "nombres", "apellidos")
    list_filter = ("estado",)

@admin.register(ContratoCore)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ("numero", "vigencia", "codigo", "fecha_inicio", "fecha_fin")
    search_fields = ("numero", "codigo")
    list_filter = ("vigencia",)

@admin.register(ColaboradorContrato)
class ColaboradorContratoAdmin(admin.ModelAdmin):
    list_display = ("colaborador", "contrato", "creado_en")
    search_fields = ("colaborador__nombres", "contrato__numero")
