# apps/dashboard/api.py

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services import fetch_dashboard_kpis


@login_required
def dashboard_kpis(request):
    """
    Endpoint principal de KPIs del dashboard.
    Retorna JSON consumible por frontend.
    """
    data = fetch_dashboard_kpis()
    return JsonResponse(data)
