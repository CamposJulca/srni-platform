from django.urls import path
from .views import list_colaboradores

app_name = "colaboradores"

urlpatterns = [
    path("", list_colaboradores, name="list"),
]
