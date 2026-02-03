from django.urls import path
from .api import kpis

urlpatterns = [
    path("kpis/", kpis, name="api_dashboard_kpis"),
]