from django.shortcuts import render
from .models import ColaboradorCore

def list_colaboradores(request):
    colaboradores = ColaboradorCore.objects.all().order_by("id")[:200]
    return render(request, "colaboradores/list.html", {"colaboradores": colaboradores})
