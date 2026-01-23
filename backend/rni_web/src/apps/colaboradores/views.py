from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection


@login_required
def colaborador_list_view(request):
    """
    Vista inicial: listado visual de colaboradores.
    Por ahora solo renderiza el template.
    """
    return render(request, "colaboradores/list.html")
