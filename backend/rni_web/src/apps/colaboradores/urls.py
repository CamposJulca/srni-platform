from django.urls import path
from . import views

app_name = "colaboradores"

urlpatterns = [
    path("", views.colaborador_list_view, name="list"),
]
