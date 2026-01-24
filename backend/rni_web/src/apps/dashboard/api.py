from django.views.decorators.http import require_GET
from .services import fetch_dashboard_kpis
from apps.accounts.api import _json_ok, _json_error  # ajusta si la ruta cambia


@require_GET
def kpis(request):
    if not request.user.is_authenticated:
        return _json_error("NOT_AUTHENTICATED", "Not authenticated.", 401)

    try:
        limit = int(request.GET.get("limit", 10))
        data = fetch_dashboard_kpis(limit_top=limit)
        return _json_ok(data)
    except Exception as e:
        return _json_error("DASHBOARD_KPIS_ERROR", str(e), 500)
