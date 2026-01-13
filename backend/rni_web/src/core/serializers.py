from rest_framework import serializers
from .models import ColaboradorCore

class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColaboradorCore
        fields = [
            "id",
            "cedula",
            "nombres",
            "apellidos",
            "estado",
            "fecha_creacion",
        ]
        read_only_fields = ("id", "fecha_creacion")
