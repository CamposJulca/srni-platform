from django.urls import path
from .api import api_login, api_logout, api_me

urlpatterns = [
    path("api/auth/login/", api_login, name="api_login"),
    path("api/auth/logout/", api_logout, name="api_logout"),
    path("api/auth/me/", api_me, name="api_me"),
]
