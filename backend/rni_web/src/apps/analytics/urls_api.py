# apps/analytics/urls_api.py
from django.urls import path
from . import api

urlpatterns = [
    path("analytics/health/", api.analytics_health, name="api_analytics_health"),
    path("analytics/sql/execute/", api.execute_sql, name="api_analytics_execute_sql"),
]
