import re
from collections import Counter
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

try:
    import pandas as pd
except ImportError as e:
    raise SystemExit(
        "Falta pandas/openpyxl en el contenedor. "
        "Agrega 'pandas' y 'openpyxl' a requirements.txt y rebuild."
    ) from e

from apps.colaboradores.models import (
    ColaboradorCore,
    ContratoCore,
    ColaboradorContrato,
    ColaboradorProcedimiento,
    Dependencia,
    Procedimiento,
    CatNivelTerritorial,
    CatDepartamento,
    CatMunicipio,
    CatRubroPresupuestal,
    CatArlRiesgo,
    CatAsignacionCarpeta,
    CatEstadoDocumentacion,
    ContratoPaaOps,
    PaaOpsObligacion,
)

# -------------------------
# Defaults para vacíos (FK NOT NULL)
# -------------------------
DEFAULT_TXT = "SIN ASIGNAR"
DEFAULT_ARL_NIVEL = 0
DEFAULT_PROC = "SIN ASIGNAR"


# -------------------------
# Helpers
# -------------------------
def norm_text(x):
    if x is None:
        return None
    s = str(x).strip()
    if s == "" or s.lower() in {"nan", "none"}:
        return None
    return re.sub(r"\s+", " ", s)


def to_int(x):
    if x is None:
        return None
    if isinstance(x, int):
        return x
    if isinstance(x, float):
        if x != x:  # NaN
            return None
        return int(x)
    s = norm_text(x)
    if not s:
        return None
    m = re.search(r"\d+", s.replace(".", "").replace(",", ""))
    return int(m.group(0)) if m else None


def to_decimal(x):
    """
    Convierte valores tipo:
    - 4042650
    - 4042650.00
    - "4.042.650,00"
    - "$ 4.042.650,00"
    - " $4,042,650.00 " (por si viene estilo US)
    a Decimal, o None si no se puede.
    """
    if x is None:
        return None

    # NaN float
    if isinstance(x, float) and (x != x):
        return None

    # Ya viene numérico
    if isinstance(x, (int, Decimal)):
        return Decimal(str(x))
    if isinstance(x, float):
        return Decimal(str(x))

    s = norm_text(x)
    if not s:
        return None

    # limpia símbolos y texto
    s = s.replace("COP", "").replace("USD", "").replace("$", "")
    s = s.replace(" ", "")

    # deja solo dígitos, separadores y signo
    s = re.sub(r"[^0-9,.\-]", "", s)

    if not s or s in {"-", ",", "."}:
        return None

    # Caso mixto (tiene . y ,) -> asumimos formato CO: 4.042.650,00
    if ("," in s) and ("." in s):
        # si la última coma está después del último punto: típico CO
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            # típico US: 4,042,650.00
            s = s.replace(",", "")
    else:
        # solo coma -> probablemente decimal
        if "," in s and "." not in s:
            s = s.replace(",", ".")

    try:
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return None


def to_date(x):
    if x is None:
        return None
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    s = norm_text(x)
    if not s:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            pass
    return None


TRUE_SET = {"ok", "si", "sí", "x", "revisado ok", "revisado", "aprobado", "cumple", "1", "true"}
FALSE_SET = {"no", "pendiente", "na", "n/a", "0", "false"}


def to_bool(x):
    s = norm_text(x)
    if s is None:
        return None
    k = s.lower()
    if k in TRUE_SET:
        return True
    if k in FALSE_SET:
        return False
    return None


def pick_sheet(xls, preferred="OPS 2026"):
    """
    Selecciona hoja:
    1) si existe preferred exacta, úsala
    2) si existe OPS_2026_limpio, úsala (tu normalizado)
    3) si existe alguna que contenga 'OPS' y '2026', úsala
    4) si no, la primera hoja
    """
    names = list(getattr(xls, "sheet_names", []))
    if not names:
        return None

    if preferred in names:
        return preferred

    if "OPS_2026_limpio" in names:
        return "OPS_2026_limpio"

    for n in names:
        u = n.upper().replace("_", " ")
        if "OPS" in u and "2026" in u:
            return n

    return names[0]


def split_obligaciones(texto: str) -> list[str]:
    """
    Intenta partir obligaciones en lista:
    - Por líneas
    - Por numeración 1., 1), 1-
    - Si no se puede, devuelve [texto]
    """
    t = norm_text(texto)
    if not t:
        return []

    raw_lines = [ln.strip() for ln in re.split(r"[\r\n]+", t) if ln.strip()]
    if len(raw_lines) >= 2:
        lines = raw_lines
    else:
        parts = re.split(r"(?:^|\s)(?=\d+\s*[\.\)\-])", t)
        lines = [p.strip() for p in parts if p.strip()]

    cleaned = []
    for ln in lines:
        ln2 = re.sub(r"^\d+\s*[\.\)\-]\s*", "", ln).strip()
        if ln2:
            cleaned.append(ln2)

    return cleaned[:200]


def safe_col(df, *names):
    """Devuelve el primer nombre de columna existente en df.columns, si no None."""
    for n in names:
        if n in df.columns:
            return n
    return None


class Command(BaseCommand):
    help = "Carga OPS 2026 desde Excel a las tablas normalizadas (solo SRNI)."

    def add_arguments(self, parser):
        parser.add_argument("excel_path", type=str, help="Ruta del .xlsx dentro del contenedor")
        parser.add_argument("--vigencia", type=int, default=2026, help="Vigencia fija (default 2026)")
        parser.add_argument("--dry-run", action="store_true", help="No escribe en BD, solo valida/contabiliza")
        parser.add_argument("--skip-obligaciones", action="store_true", help="No crea filas en paa_ops_obligacion")
        parser.add_argument("--skip-vinculos", action="store_true", help="No crea filas en colaborador_contrato")
        parser.add_argument("--skip-procedimientos", action="store_true", help="No crea filas en colaborador_procedimiento")
        parser.add_argument("--limit", type=int, default=None, help="Procesa solo N filas (debug)")

    @transaction.atomic
    def handle(self, *args, **opts):
        excel_path = opts["excel_path"]
        vigencia = opts["vigencia"]
        dry_run = opts["dry_run"]
        skip_obl = opts["skip_obligaciones"]
        skip_vinc = opts["skip_vinculos"]
        skip_proc_vinc = opts["skip_procedimientos"]
        limit = opts["limit"]

        xls = pd.ExcelFile(excel_path)
        sheet = pick_sheet(xls, preferred="OPS 2026")
        if not sheet:
            raise SystemExit("El archivo no tiene hojas legibles.")

        df = pd.read_excel(excel_path, sheet_name=sheet)
        df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]

        col_numero = "ID 2026"
        if col_numero not in df.columns:
            raise SystemExit(f"No existe la columna requerida '{col_numero}'. Columnas: {list(df.columns)}")

        # municipio a veces viene mal tipeado
        col_muni = safe_col(df, "MUNICIPIO EJECUCION", "MUNICIPIO EJECUCUCION")

        if limit:
            df = df.head(limit)

        total = len(df.index)
        self.stdout.write(self.style.SUCCESS(f"Hoja: {sheet} | Filas leídas: {total}"))
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN: no se escribirá nada en BD."))

        # =================
        # 0) Asegurar defaults NOT NULL
        # =================
        if not dry_run:
            CatRubroPresupuestal.objects.get_or_create(codigo=DEFAULT_TXT, defaults={"descripcion": DEFAULT_TXT, "activo": True})
            CatAsignacionCarpeta.objects.get_or_create(nombre=DEFAULT_TXT, defaults={"activo": True})
            CatEstadoDocumentacion.objects.get_or_create(nombre=DEFAULT_TXT, defaults={"orden": 999, "activo": True})
            Procedimiento.objects.get_or_create(nombre=DEFAULT_PROC)
            CatArlRiesgo.objects.get_or_create(nivel=DEFAULT_ARL_NIVEL, defaults={"descripcion": DEFAULT_TXT, "activo": True})

        # =================
        # 1) CATÁLOGOS
        # =================
        def _goc(model, **kwargs):
            if dry_run:
                return None, True
            return model.objects.get_or_create(**kwargs)

        for v in set(df.get("NIVEL CENTRAL/TERRITORIAL", pd.Series(dtype=str)).dropna().astype(str)):
            name = norm_text(v)
            if name:
                _goc(CatNivelTerritorial, nombre=name)

        for v in set(df.get("DEPARTAMENTO EJECUCION", pd.Series(dtype=str)).dropna().astype(str)):
            name = norm_text(v)
            if name:
                _goc(CatDepartamento, nombre=name)

        if "DEPARTAMENTO EJECUCION" in df.columns and col_muni:
            for _, r in df[["DEPARTAMENTO EJECUCION", col_muni]].dropna().iterrows():
                depto_name = norm_text(r["DEPARTAMENTO EJECUCION"])
                muni_name = norm_text(r[col_muni])
                if not depto_name or not muni_name:
                    continue
                if not dry_run:
                    depto = CatDepartamento.objects.get(nombre=depto_name)
                    CatMunicipio.objects.get_or_create(departamento=depto, nombre=muni_name)

        # Rubro (con default si viene vacío)
        rubros = df.get("RUBRO PRESUPUESTAL", pd.Series(dtype=str))
        for v in set(rubros.dropna().astype(str)):
            code = norm_text(v)
            if code:
                _goc(CatRubroPresupuestal, codigo=code)

        # ARL (con default si viene vacío)
        arls = df.get("NIVEL RIESGO ARL", pd.Series(dtype=object))
        for v in set(arls.dropna()):
            nivel = to_int(v)
            if nivel is not None:
                _goc(CatArlRiesgo, nivel=nivel)

        carpetas = df.get("ASIGNACIÓN CARPETA", pd.Series(dtype=str))
        for v in set(carpetas.dropna().astype(str)):
            name = norm_text(v)
            if name:
                _goc(CatAsignacionCarpeta, nombre=name)

        estados = df.get("ESTADO DOCUMENTACIÓN", pd.Series(dtype=str))
        for v in set(estados.dropna().astype(str)):
            name = norm_text(v)
            if name:
                _goc(CatEstadoDocumentacion, nombre=name)

        self.stdout.write(self.style.SUCCESS("Catálogos OK"))

        # =================
        # 2) MAESTRAS
        # =================
        for _, r in df[["DEPENDENCIA", "DEPENDENCIA ASOCIADA"]].iterrows():
            padre_name = norm_text(r.get("DEPENDENCIA"))
            hijo_name = norm_text(r.get("DEPENDENCIA ASOCIADA"))

            if dry_run:
                continue

            padre = None
            if padre_name:
                padre, _ = Dependencia.objects.get_or_create(nombre=padre_name)

            if hijo_name:
                obj, created = Dependencia.objects.get_or_create(
                    nombre=hijo_name,
                    defaults={"dependencia_padre": padre},
                )
                if (not created) and padre and obj.dependencia_padre_id != padre.id:
                    obj.dependencia_padre = padre
                    obj.save(update_fields=["dependencia_padre"])

        for v in set(df.get("PROCEDIMIENTO", pd.Series(dtype=str)).dropna().astype(str)):
            name = norm_text(v)
            if name and not dry_run:
                Procedimiento.objects.get_or_create(nombre=name)

        for _, r in df[["NUMERO DE CEDULA", "NOMBRES CONTRATISTA", "APELLIDOS CONTRATISTA"]].iterrows():
            ced = to_int(r.get("NUMERO DE CEDULA"))
            if ced is None:
                continue
            if dry_run:
                continue
            nombres = norm_text(r.get("NOMBRES CONTRATISTA")) or ""
            apellidos = norm_text(r.get("APELLIDOS CONTRATISTA")) or ""
            ColaboradorCore.objects.update_or_create(
                cedula=str(ced),
                defaults={"nombres": nombres, "apellidos": apellidos, "estado": "ACTIVO"},
            )

        default_ini = date(vigencia, 1, 1)
        default_fin = date(vigencia, 12, 31)

        for _, r in df[[col_numero]].iterrows():
            numero = to_int(r.get(col_numero))
            if numero is None:
                continue
            if dry_run:
                continue
            ContratoCore.objects.get_or_create(
                numero=numero,
                vigencia=vigencia,
                defaults={
                    "codigo": f"OPS-{numero}-{vigencia}",
                    "fecha_inicio": default_ini,
                    "fecha_fin": default_fin,
                },
            )

        self.stdout.write(self.style.SUCCESS("Maestras OK"))

        # =========================
        # 3) TRANSACCIONAL: contrato_paa_ops
        # =========================
        creados = 0
        actualizados = 0
        saltados = 0
        razones = Counter()

        for _, r in df.iterrows():
            numero = to_int(r.get(col_numero))
            if numero is None:
                saltados += 1
                razones["sin_numero_contrato(ID 2026)"] += 1
                continue

            ced = to_int(r.get("NUMERO DE CEDULA"))
            if ced is None:
                saltados += 1
                razones["sin_cedula"] += 1
                continue

            if dry_run:
                continue

            try:
                contrato = ContratoCore.objects.get(numero=numero, vigencia=vigencia)
            except ContratoCore.DoesNotExist:
                saltados += 1
                razones["contrato_no_existe"] += 1
                continue

            try:
                colaborador = ColaboradorCore.objects.get(cedula=str(ced))
            except ColaboradorCore.DoesNotExist:
                saltados += 1
                razones["colaborador_no_existe"] += 1
                continue

            dep_name = norm_text(r.get("DEPENDENCIA"))
            if not dep_name:
                saltados += 1
                razones["sin_dependencia"] += 1
                continue

            dep_asoc_name = norm_text(r.get("DEPENDENCIA ASOCIADA"))

            try:
                dependencia = Dependencia.objects.get(nombre=dep_name)
            except Dependencia.DoesNotExist:
                saltados += 1
                razones["dependencia_no_existe"] += 1
                continue

            dependencia_asociada = None
            if dep_asoc_name:
                dependencia_asociada = Dependencia.objects.filter(nombre=dep_asoc_name).first()

            # Catálogos (con defaults)
            nivel_name = norm_text(r.get("NIVEL CENTRAL/TERRITORIAL"))
            depto_name = norm_text(r.get("DEPARTAMENTO EJECUCION"))
            muni_name = norm_text(r.get(col_muni)) if col_muni else None

            proc_name = norm_text(r.get("PROCEDIMIENTO")) or DEFAULT_PROC
            rubro_code = norm_text(r.get("RUBRO PRESUPUESTAL")) or DEFAULT_TXT
            arl_nivel = to_int(r.get("NIVEL RIESGO ARL"))
            if arl_nivel is None:
                arl_nivel = DEFAULT_ARL_NIVEL
            carpeta_name = norm_text(r.get("ASIGNACIÓN CARPETA")) or DEFAULT_TXT
            estado_doc_name = norm_text(r.get("ESTADO DOCUMENTACIÓN")) or DEFAULT_TXT

            missing = []
            for k, v in {
                "nivel": nivel_name,
                "depto": depto_name,
                "muni": muni_name,
            }.items():
                if v in (None, ""):
                    missing.append(k)

            if missing:
                saltados += 1
                razones["faltan_geo:" + ",".join(missing)] += 1
                continue

            try:
                nivel = CatNivelTerritorial.objects.get(nombre=nivel_name)
                depto = CatDepartamento.objects.get(nombre=depto_name)
                muni = CatMunicipio.objects.get(departamento=depto, nombre=muni_name)

                proc = Procedimiento.objects.get(nombre=proc_name)
                rubro = CatRubroPresupuestal.objects.get(codigo=rubro_code)
                arl = CatArlRiesgo.objects.get(nivel=arl_nivel)
                carpeta = CatAsignacionCarpeta.objects.get(nombre=carpeta_name)
                estado_doc = CatEstadoDocumentacion.objects.get(nombre=estado_doc_name)
            except Exception:
                saltados += 1
                razones["lookup_catalogos_fallo"] += 1
                continue

            defaults = {
                "colaborador": colaborador,
                "dependencia": dependencia,
                "dependencia_asociada": dependencia_asociada,
                "procedimiento": proc,
                "nivel_territorial": nivel,
                "departamento_ejecucion": depto,
                "municipio_ejecucion": muni,
                "rubro_presupuestal": rubro,
                "arl_riesgo": arl,
                "asignacion_carpeta": carpeta,
                "estado_documentacion": estado_doc,
                "objeto_paa": norm_text(r.get("OBJETO PAA")) or "",
                "requisitos_academicos_inicial": norm_text(r.get("REQUSITOS ACADEMICOS")),
                "experiencia_minima_meses": to_int(r.get("EXPERIENCIA MINIMA REQUERIDA (MESES)")),
                "fecha_inicio_estimada": to_date(r.get("FECHA ESTIMADA INICIO CONTRATO")),
                "fecha_fin_estimada": to_date(r.get("FECHA TERMINACION CONTRATO")),
                "honorarios_mensuales_estimados": to_decimal(r.get("VALOR HONORARIOS MENSUALES ESTIMADOS")),
                "requisitos_academicos_final": norm_text(r.get("REQUISITOS ACADÉMICOS FINAL")),
                "experiencia_definitiva": norm_text(r.get("EXPERIENCIA DEFINITIVA")),
                "honorarios_segun_perfil": to_decimal(r.get("HONORARIOS SEGÚN PERFIL")),
                "supervisor_nombre": norm_text(r.get("NOMBRE SUPERVISOR")),
                "supervisor_cargo": norm_text(r.get("CARGO SUPERVISOR")),
                "doc_estudio_previo": to_bool(r.get("ESTUDIO PREVIO")),
                "doc_memorando_solicitud": to_bool(r.get("MEMORANDO DE SOLICITUD")),
                "doc_hoja_vida_sigep": to_bool(r.get("HOJA DE VIDA SIGEP")),
                "observacion": norm_text(r.get("OBSERVACION")),
                "obligaciones_text": norm_text(r.get("OBLIGACIONES")),
            }

            try:
                obj, created = ContratoPaaOps.objects.update_or_create(
                    contrato=contrato,
                    defaults=defaults,
                )
            except IntegrityError:
                saltados += 1
                razones["integrity_error_paa_ops"] += 1
                continue

            if created:
                creados += 1
            else:
                actualizados += 1

            # Vinculo colaborador_contrato
            if not skip_vinc:
                fi = defaults["fecha_inicio_estimada"] or default_ini
                ff = defaults["fecha_fin_estimada"]
                ColaboradorContrato.objects.get_or_create(
                    colaborador=colaborador,
                    contrato=contrato,
                    defaults={"estado": "ACTIVO", "fecha_inicio": fi, "fecha_fin": ff},
                )

            # Vinculo colaborador_procedimiento
            if not skip_proc_vinc:
                ColaboradorProcedimiento.objects.get_or_create(
                    colaborador=colaborador,
                    procedimiento=proc,
                    defaults={"estado": "ACTIVO", "observaciones": "Cargado desde OPS 2026"},
                )

            # Obligaciones
            if not skip_obl:
                texto_obl = defaults.get("obligaciones_text")
                items = split_obligaciones(texto_obl)
                if items:
                    PaaOpsObligacion.objects.filter(contrato_paa_ops=obj).delete()
                    for i, desc in enumerate(items, start=1):
                        PaaOpsObligacion.objects.create(
                            contrato_paa_ops=obj,
                            orden=i,
                            descripcion=desc,
                        )

        self.stdout.write(self.style.SUCCESS(
            f"contrato_paa_ops -> creados={creados}, actualizados={actualizados}, saltados={saltados}"
        ))

        if razones:
            self.stdout.write(self.style.WARNING("Top razones de saltados:"))
            for k, v in razones.most_common(20):
                self.stdout.write(f"  - {k}: {v}")

        self.stdout.write(self.style.SUCCESS("Carga completa ✅"))