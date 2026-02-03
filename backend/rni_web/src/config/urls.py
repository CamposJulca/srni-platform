from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("auth/", include("apps.accounts.urls")),          # UI
    path("api/auth/", include("apps.accounts.urls_api")), # API

    path("api/", include("core.urls")),

    path("api/sinapsis/", include("sinapsis.urls")),
]
