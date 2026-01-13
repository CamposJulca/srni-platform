from django import forms
from .models import ColaboradorCore

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = ColaboradorCore
        fields = ["cedula", "nombres", "apellidos", "estado"]
