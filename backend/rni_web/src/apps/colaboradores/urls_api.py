from django.urls import path
from . import api

urlpatterns = [
    path("colaboradores/", api.colaboradores_list_create, name="api_colaboradores_list_create"),
    path("colaboradores/<int:pk>/", api.colaboradores_detail, name="api_colaboradores_detail"),
    
]
