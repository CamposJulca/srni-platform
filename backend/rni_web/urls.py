from django.urls import path, include

urlpatterns = [
    path("api/sinapsis/", include("sinapsis.urls")),
]
