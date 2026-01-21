# src/sinapsis/views.py

from django.http import JsonResponse
from django.views import View

from .repositories import MongoSinapsisSnapshotRepository


class ProjectSummaryListView(View):
    """
    API: devuelve una vista plana de proyectos SINAPSIS
    """

    def get(self, request, *args, **kwargs):
        repo = MongoSinapsisSnapshotRepository()
        data = repo.list_project_summaries()
        return JsonResponse(data, safe=False)
