from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # API actual (no se toca)
    path("api/", include("core.api_urls")),

    # Legacy UI (migrado de rediapp)
    path("", include("apps.accounts.urls")),
    path("analytics/", include("apps.analytics.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("colaboradores/", include("apps.colaboradores.urls")),
    path("automatizacion/", include("apps.automatizacion_documental.urls")),
   
]

# Media (si usas uploads en local)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
