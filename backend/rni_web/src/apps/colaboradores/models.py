from django.db import models
from django.db.models import Q

# =========================
# CORE / MAESTRAS
# =========================

class ColaboradorCore(models.Model):
    cedula = models.CharField(max_length=30, unique=True)
    nombres = models.TextField()
    apellidos = models.TextField()
    estado = models.CharField(max_length=30, default="ACTIVO")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "colaborador_core"
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        indexes = [
            models.Index(fields=["cedula"], name="ix_colaborador_cedula"),
        ]

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Dependencia(models.Model):
    nombre = models.CharField(max_length=255)
    dependencia_asociada = models.TextField(null=True, blank=True)
    dependencia_padre = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="hijos",
        db_column="dependencia_padre_id",
    )

    class Meta:
        db_table = "dependencia"
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"
        indexes = [
            models.Index(fields=["nombre"], name="ix_dependencia_nombre"),
        ]

    def __str__(self):
        return self.nombre


class Procedimiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "procedimiento"
        verbose_name = "Procedimiento"
        verbose_name_plural = "Procedimientos"

    def __str__(self):
        return self.nombre

class ContratoCore(models.Model):
    numero = models.IntegerField()
    vigencia = models.IntegerField()

    codigo = models.CharField(max_length=100, null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "contrato_core"
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        constraints = [
            models.UniqueConstraint(
                fields=["numero", "vigencia"],
                name="uq_contrato_core_numero_vigencia",
            ),
        ]
        indexes = [
            models.Index(fields=["numero", "vigencia"], name="ix_contrato_num_vig"),
        ]

    def __str__(self):
        return f"Contrato {self.numero} / {self.vigencia}"


class ColaboradorContrato(models.Model):
    colaborador = models.ForeignKey(
        ColaboradorCore,
        on_delete=models.PROTECT,
        db_column="colaborador_id",
        related_name="contratos_vinculados",
    )
    contrato = models.ForeignKey(
        ContratoCore,
        on_delete=models.PROTECT,
        db_column="contrato_id",
        related_name="colaboradores_vinculados",
    )
    estado = models.CharField(max_length=30, default="ACTIVO")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "colaborador_contrato"
        verbose_name = "Vinculación contractual"
        verbose_name_plural = "Vinculaciones contractuales"
        indexes = [
            models.Index(fields=["colaborador"], name="ix_colab_contrato_colab"),
            models.Index(fields=["contrato"], name="ix_colab_contrato_contr"),
        ]

    def __str__(self):
        return f"{self.colaborador_id} -> {self.contrato_id} ({self.estado})"


class ColaboradorProcedimiento(models.Model):
    colaborador = models.ForeignKey(
        ColaboradorCore,
        on_delete=models.PROTECT,
        db_column="colaborador_id",
        related_name="procedimientos_vinculados",
    )
    procedimiento = models.ForeignKey(
        Procedimiento,
        on_delete=models.PROTECT,
        db_column="procedimiento_id",
        related_name="colaboradores_vinculados",
    )
    fecha_asignacion = models.DateField(auto_now_add=True)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=30, default="ACTIVO")
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "colaborador_procedimiento"
        verbose_name = "Colaborador por procedimiento"
        verbose_name_plural = "Colaboradores por procedimiento"
        indexes = [
            models.Index(fields=["colaborador"], name="ix_colab_proc_colab"),
            models.Index(fields=["procedimiento"], name="ix_colab_proc_proc"),
        ]


# =========================
# CATÁLOGOS (SELECTS)
# =========================

class CatNivelTerritorial(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "cat_nivel_territorial"
        verbose_name = "Nivel territorial"
        verbose_name_plural = "Niveles territoriales"

    def __str__(self):
        return self.nombre


class CatDepartamento(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    codigo_dane = models.CharField(max_length=10, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "cat_departamento"
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nombre


class CatMunicipio(models.Model):
    departamento = models.ForeignKey(
        CatDepartamento,
        on_delete=models.PROTECT,
        db_column="departamento_id",
        related_name="municipios",
    )
    nombre = models.CharField(max_length=120)
    codigo_dane = models.CharField(max_length=10, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "cat_municipio"
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        constraints = [
            models.UniqueConstraint(
                fields=["departamento", "nombre"],
                name="uq_municipio_depto_nombre",
            )
        ]
        indexes = [
            models.Index(fields=["departamento", "nombre"], name="ix_municipio_depto_nom"),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.departamento.nombre})"


class CatRubroPresupuestal(models.Model):
    codigo = models.CharField(max_length=60, unique=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cat_rubro_presupuestal"
        verbose_name = "Rubro presupuestal"
        verbose_name_plural = "Rubros presupuestales"

    def __str__(self):
        return self.codigo


class CatArlRiesgo(models.Model):
    nivel = models.SmallIntegerField(unique=True)
    descripcion = models.CharField(max_length=120, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "cat_arl_riesgo"
        verbose_name = "ARL Riesgo"
        verbose_name_plural = "ARL Riesgos"

    def __str__(self):
        return str(self.nivel)


class CatEstadoDocumentacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    orden = models.SmallIntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "cat_estado_documentacion"
        verbose_name = "Estado documentación"
        verbose_name_plural = "Estados documentación"

    def __str__(self):
        return self.nombre


class CatAsignacionCarpeta(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "cat_asignacion_carpeta"
        verbose_name = "Asignación carpeta"
        verbose_name_plural = "Asignaciones carpeta"

    def __str__(self):
        return self.nombre


# =========================
# TRANSACCIONAL: DETALLE PAA/OPS
# =========================

class ContratoPaaOps(models.Model):
    contrato = models.ForeignKey(
        ContratoCore,
        on_delete=models.PROTECT,
        db_column="contrato_id",
        related_name="paa_ops",
    )

    colaborador = models.ForeignKey(
        ColaboradorCore,
        on_delete=models.PROTECT,
        db_column="colaborador_id",
        related_name="paa_ops",
    )

    dependencia = models.ForeignKey(
        Dependencia,
        on_delete=models.PROTECT,
        db_column="dependencia_id",
        related_name="paa_ops",
    )

    dependencia_asociada = models.ForeignKey(
        Dependencia,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="dependencia_asociada_id",
        related_name="paa_ops_asociadas",
    )

    procedimiento = models.ForeignKey(
        Procedimiento,
        on_delete=models.PROTECT,
        db_column="procedimiento_id",
        related_name="paa_ops",
    )

    nivel_territorial = models.ForeignKey(
        CatNivelTerritorial,
        on_delete=models.PROTECT,
        db_column="nivel_territorial_id",
        related_name="paa_ops",
    )

    departamento_ejecucion = models.ForeignKey(
        CatDepartamento,
        on_delete=models.PROTECT,
        db_column="departamento_ejecucion_id",
        related_name="paa_ops",
    )

    municipio_ejecucion = models.ForeignKey(
        CatMunicipio,
        on_delete=models.PROTECT,
        db_column="municipio_ejecucion_id",
        related_name="paa_ops",
    )

    rubro_presupuestal = models.ForeignKey(
        CatRubroPresupuestal,
        on_delete=models.PROTECT,
        db_column="rubro_presupuestal_id",
        related_name="paa_ops",
    )

    arl_riesgo = models.ForeignKey(
        CatArlRiesgo,
        on_delete=models.PROTECT,
        db_column="arl_riesgo_id",
        related_name="paa_ops",
    )

    asignacion_carpeta = models.ForeignKey(
        CatAsignacionCarpeta,
        on_delete=models.PROTECT,
        db_column="asignacion_carpeta_id",
        related_name="paa_ops",
    )

    estado_documentacion = models.ForeignKey(
        CatEstadoDocumentacion,
        on_delete=models.PROTECT,
        db_column="estado_documentacion_id",
        related_name="paa_ops",
    )

    objeto_paa = models.TextField()
    requisitos_academicos_inicial = models.TextField(null=True, blank=True)
    experiencia_minima_meses = models.IntegerField(null=True, blank=True)

    fecha_inicio_estimada = models.DateField(null=True, blank=True)
    fecha_fin_estimada = models.DateField(null=True, blank=True)

    honorarios_mensuales_estimados = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    requisitos_academicos_final = models.TextField(null=True, blank=True)
    experiencia_definitiva = models.TextField(null=True, blank=True)
    honorarios_segun_perfil = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )

    supervisor_nombre = models.CharField(max_length=160, null=True, blank=True)
    supervisor_cargo = models.CharField(max_length=160, null=True, blank=True)

    doc_estudio_previo = models.BooleanField(null=True, blank=True)
    doc_memorando_solicitud = models.BooleanField(null=True, blank=True)
    doc_hoja_vida_sigep = models.BooleanField(null=True, blank=True)

    observacion = models.TextField(null=True, blank=True)
    obligaciones_text = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "contrato_paa_ops"
        verbose_name = "Contrato PAA/OPS"
        verbose_name_plural = "Contratos PAA/OPS"
        constraints = [
            # 1 registro PAA/OPS por contrato:
            models.UniqueConstraint(fields=["contrato"], name="uq_contrato_paa_ops_contrato"),
            # experiencia no negativa
            models.CheckConstraint(
                check=Q(experiencia_minima_meses__gte=0) | Q(experiencia_minima_meses__isnull=True),
                name="ck_paa_ops_experiencia_no_negativa",
            ),
        ]
        indexes = [
            models.Index(fields=["contrato"], name="ix_paa_ops_contrato"),
            models.Index(fields=["colaborador"], name="ix_paa_ops_colaborador"),
            models.Index(fields=["dependencia"], name="ix_paa_ops_dependencia"),
            models.Index(fields=["procedimiento"], name="ix_paa_ops_procedimiento"),
            models.Index(fields=["estado_documentacion"], name="ix_paa_ops_estado_doc"),
            models.Index(fields=["rubro_presupuestal"], name="ix_paa_ops_rubro"),
            models.Index(fields=["fecha_inicio_estimada"], name="ix_paa_ops_f_ini"),
            models.Index(fields=["fecha_fin_estimada"], name="ix_paa_ops_f_fin"),
        ]


class PaaOpsObligacion(models.Model):
    contrato_paa_ops = models.ForeignKey(
        ContratoPaaOps,
        on_delete=models.CASCADE,
        db_column="contrato_paa_ops_id",
        related_name="obligaciones",
    )
    orden = models.IntegerField()
    descripcion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "paa_ops_obligacion"
        verbose_name = "Obligación PAA/OPS"
        verbose_name_plural = "Obligaciones PAA/OPS"
        indexes = [
            models.Index(fields=["contrato_paa_ops", "orden"], name="ix_oblig_paa_ops_orden"),
        ]

    def __str__(self):
        return f"{self.contrato_paa_ops_id} - {self.orden}"