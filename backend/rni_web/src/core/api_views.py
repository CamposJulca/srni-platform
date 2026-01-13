from rest_framework import generics
from .models import ColaboradorCore
from .serializers import ColaboradorSerializer

class ColaboradorListCreateView(generics.ListCreateAPIView):
    queryset = ColaboradorCore.objects.all()
    serializer_class = ColaboradorSerializer


class ColaboradorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ColaboradorCore.objects.all()
    serializer_class = ColaboradorSerializer
