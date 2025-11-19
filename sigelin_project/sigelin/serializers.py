from rest_framework import viewsets
from .models import Equipos  # clase generada por inspectdb
from .serializers import EquipoModelSerializer  # ModelSerializer basado en Equipos

class EquiposViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Equipos.objects.filter(activo=True)
    serializer_class = EquipoModelSerializer
