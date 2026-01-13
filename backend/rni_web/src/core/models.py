from django.db import models

# Create your models here.
from django.db import models

class ColaboradorCore(models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=20, unique=True)
    nombres = models.TextField()
    apellidos = models.TextField()
    estado = models.CharField(max_length=20, blank=True, null=True)
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "colaborador_core"
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ContratoCore(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    vigencia = models.IntegerField()
    codigo = models.CharField(max_length=50, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "contrato_core"
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"

    def __str__(self):
        return f"Contrato {self.numero} / {self.vigencia}"

class ColaboradorContrato(models.Model):
    id = models.AutoField(primary_key=True)
    colaborador = models.ForeignKey(
        ColaboradorCore,
        on_delete=models.CASCADE,
        db_column="colaborador_id"
    )
    contrato = models.ForeignKey(
        ContratoCore,
        on_delete=models.CASCADE,
        db_column="contrato_id"
    )
    creado_en = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "colaborador_contrato"
        verbose_name = "Vinculación contractual"
        verbose_name_plural = "Vinculaciones contractuales"
