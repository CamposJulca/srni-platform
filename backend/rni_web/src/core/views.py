from django.shortcuts import render, redirect
from .models import ColaboradorCore
from .forms import ColaboradorForm
from rest_framework import viewsets
from .serializers import ColaboradorSerializer

class ColaboradorViewSet(viewsets.ModelViewSet):
    queryset = ColaboradorCore.objects.all()
    serializer_class = ColaboradorSerializer


def colaborador_list(request):
    colaboradores = ColaboradorCore.objects.all()
    return render(request, "core/colaborador_list.html", {
        "colaboradores": colaboradores
    })

def colaborador_create(request):
    form = ColaboradorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("colaborador_list")
    return render(request, "core/colaborador_form.html", {"form": form})

def colaborador_update(request, pk):
    colaborador = ColaboradorCore.objects.get(pk=pk)
    form = ColaboradorForm(request.POST or None, instance=colaborador)
    if form.is_valid():
        form.save()
        return redirect("colaborador_list")
    return render(request, "core/colaborador_form.html", {"form": form})

def colaborador_delete(request, pk):
    colaborador = ColaboradorCore.objects.get(pk=pk)
    if request.method == "POST":
        colaborador.delete()
        return redirect("colaborador_list")
    return render(request, "core/colaborador_confirm_delete.html", {"obj": colaborador})
