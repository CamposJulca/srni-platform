from django.urls import path
from .api_views import (
    ColaboradorListCreateView,
    ColaboradorDetailView,
)

urlpatterns = [
    path("colaboradores/", ColaboradorListCreateView.as_view()),
    path("colaboradores/<int:pk>/", ColaboradorDetailView.as_view()),
]
