from django.urls import path
from .views import ProjectSummaryListView

urlpatterns = [
    path("projects/", ProjectSummaryListView.as_view(), name="sinapsis-projects"),
]
