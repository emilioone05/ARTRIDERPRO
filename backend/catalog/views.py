from rest_framework import viewsets, permissions, filters 
from django_filters.rest_framework import DjangoFilterBackend
from .models import Equipo
from .serializers import EquipoSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # ACTIVA LOS FILTROS AQUÍ
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # 1. Filtrado exacto (ej: ?categoria=1)
    filterset_fields = ['categoria', 'propietario']
    
    # 2. Búsqueda de texto (ej: ?search=JBL)
    search_fields = ['titulo', 'descripcion']
    
    # 3. Ordenamiento (ej: ?ordering=precio)
    ordering_fields = ['created_at']