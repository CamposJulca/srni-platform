from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include([
        # Rutas API del sistema de autenticación
        path("auth/", include("apps.accounts.urls_api")),

        # Rutas API del dashboard
        path("dashboard/", include("apps.dashboard.urls_api")),



        path("colaboradores/", include("core.api_urls")),
        path("sinapsis/", include("sinapsis.urls")),
    ])),
]
