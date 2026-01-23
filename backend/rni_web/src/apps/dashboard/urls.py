# apps/dashboard/urls.py

from django.urls import path
from . import views

app_name = "dashboard"   # 🔴 SIN ESTO NO EXISTE EL NAMESPACE

urlpatterns = [
    path("", views.dashboard_view, name="home"),
]
