from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include([
        path("auth/", include("apps.accounts.urls_api")),
        path("colaboradores/", include("core.api_urls")),
        path("sinapsis/", include("sinapsis.urls")),
    ])),
]
