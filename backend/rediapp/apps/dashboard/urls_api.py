from django.urls import path
from .api import kpis

urlpatterns = [
    path("api/dashboard/kpis/", kpis, name="api_dashboard_kpis"),
]
