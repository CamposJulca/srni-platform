# apps/colaboradores/api.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from core.models import ColaboradorCore


def _json_error(code: str, message: str, status: int):
    return JsonResponse(
        {"ok": False, "data": None, "error": {"code": code, "message": message}},
        status=status,
    )


def _json_ok(data=None, status: int = 200):
    return JsonResponse({"ok": True, "data": data, "error": None}, status=status)


def _parse_json(request):
    try:
        raw = request.body.decode("utf-8-sig")
        return json.loads(raw or "{}"), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _serialize_colaborador(obj: ColaboradorCore):
    fc = obj.fecha_creacion
    if fc and timezone.is_naive(fc):
        fc = timezone.make_aware(fc, timezone.get_current_timezone())
    return {
        "id": obj.id,
        "cedula": obj.cedula,
        "nombres": obj.nombres,
        "apellidos": obj.apellidos,
        "estado": obj.estado,
        "fecha_creacion": fc.isoformat() if fc else None,
    }

@login_required
@require_http_methods(["GET", "POST"])
def colaboradores_list_create(request):
    # GET: list con paginación simple
    if request.method == "GET":
        page = int(request.GET.get("page", 1) or 1)
        page_size = int(request.GET.get("page_size", 20) or 20)
        q = (request.GET.get("q") or "").strip()
        estado = (request.GET.get("estado") or "").strip()

        qs = ColaboradorCore.objects.all().order_by("id")
        if q:
            qs = qs.filter(nombres__icontains=q) | qs.filter(apellidos__icontains=q) | qs.filter(cedula__icontains=q)
        if estado:
            qs = qs.filter(estado__iexact=estado)

        total = qs.count()
        total_pages = max(1, (total + page_size - 1) // page_size)
        page = max(1, min(page, total_pages))

        start = (page - 1) * page_size
        end = start + page_size
        items = [_serialize_colaborador(x) for x in qs[start:end]]

        return _json_ok(
            {
                "items": items,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "total_pages": total_pages,
                },
                "filters": {"q": q, "estado": estado},
            }
        )

    # POST: create
    payload, err = _parse_json(request)
    if err:
        return _json_error("INVALID_JSON", f"Invalid JSON body. Detail: {err}", 400)

    cedula = (payload.get("cedula") or "").strip()
    nombres = (payload.get("nombres") or "").strip()
    apellidos = (payload.get("apellidos") or "").strip()
    estado = (payload.get("estado") or "ACTIVO").strip()

    if not cedula or not nombres or not apellidos:
        return _json_error("VALIDATION_ERROR", "cedula, nombres, apellidos are required.", 400)

    if ColaboradorCore.objects.filter(cedula=cedula).exists():
        return _json_error("DUPLICATE", "cedula already exists.", 409)

    obj = ColaboradorCore.objects.create(
        cedula=cedula,
        nombres=nombres,
        apellidos=apellidos,
        estado=estado,
    )
    return _json_ok(_serialize_colaborador(obj), status=201)


@login_required
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def colaboradores_detail(request, pk: int):
    try:
        obj = ColaboradorCore.objects.get(pk=pk)
    except ColaboradorCore.DoesNotExist:
        return _json_error("NOT_FOUND", "Colaborador not found.", 404)

    if request.method == "GET":
        return _json_ok(_serialize_colaborador(obj))

    if request.method in ("PUT", "PATCH"):
        payload, err = _parse_json(request)
        if err:
            return _json_error("INVALID_JSON", f"Invalid JSON body. Detail: {err}", 400)

        # Solo permitimos editar estos campos
        for field in ("cedula", "nombres", "apellidos", "estado"):
            if field in payload and payload[field] is not None:
                setattr(obj, field, str(payload[field]).strip())

        # validación mínima
        if not obj.cedula or not obj.nombres or not obj.apellidos:
            return _json_error("VALIDATION_ERROR", "cedula, nombres, apellidos cannot be empty.", 400)

        # cedula unique
        if ColaboradorCore.objects.exclude(pk=obj.pk).filter(cedula=obj.cedula).exists():
            return _json_error("DUPLICATE", "cedula already exists.", 409)

        obj.save()
        return _json_ok(_serialize_colaborador(obj))

    # DELETE
    obj.delete()
    return _json_ok({"deleted": True, "id": pk})
