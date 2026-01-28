from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # APIs
    path("api/", include("core.api_urls")),
    path("api/sinapsis/", include("sinapsis.urls")),
]
