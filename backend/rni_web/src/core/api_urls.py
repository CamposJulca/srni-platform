from django.urls import path
from .api_views import (
    ColaboradorListCreateView,
    ColaboradorDetailView,
)

urlpatterns = [
    path("colaboradores/", ColaboradorListCreateView.as_view(), name="api_colaborador_list"),
    path("colaboradores/<int:pk>/", ColaboradorDetailView.as_view(), name="api_colaborador_detail"),
]
