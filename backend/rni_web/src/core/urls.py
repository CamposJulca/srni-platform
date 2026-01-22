from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColaboradorViewSet

router = DefaultRouter()
router.register(r"colaboradores", ColaboradorViewSet, basename="colaborador")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", include("apps.accounts.urls_api")),
]
