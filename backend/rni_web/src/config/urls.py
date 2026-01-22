from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.accounts.urls")),
    path("", include("apps.accounts.urls_api")),
    path("", include("apps.dashboard.urls")),
    path("colaboradores/", include("apps.colaboradores.urls")),
]
