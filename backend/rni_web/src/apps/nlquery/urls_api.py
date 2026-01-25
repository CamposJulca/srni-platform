# apps/nlquery/urls_api.py
from django.urls import path
from . import api

urlpatterns = [
    path("nlquery/health/", api.health, name="api_nlquery_health"),
    path("nlquery/schema/", api.schema, name="api_nlquery_schema"),
    path("nlquery/generate-sql/", api.generate_sql, name="api_nlquery_generate_sql"),
    path("nlquery/run/", api.run_query, name="api_nlquery_run"),
]
