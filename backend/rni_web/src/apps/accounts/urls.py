from django.urls import path
from .views import RniLoginView, home_view

urlpatterns = [
    path('login/', RniLoginView.as_view(), name='login'),
    path('', home_view, name='home'),
]
