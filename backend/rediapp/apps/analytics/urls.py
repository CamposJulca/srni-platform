from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("", views.sql_query_view, name="sql_query"),
]
