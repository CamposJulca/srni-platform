from django.urls import path
from .api import execute_sql

urlpatterns = [
    path("api/sql/execute/", execute_sql, name="api_execute_sql"),
]