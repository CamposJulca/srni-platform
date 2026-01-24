from django.urls import path
from .api import api_csrf, api_login, api_logout, api_me

urlpatterns = [
    path("csrf/", api_csrf, name="api_csrf"),
    path("login/", api_login, name="api_login"),
    path("logout/", api_logout, name="api_logout"),
    path("me/", api_me, name="api_me"),
]
