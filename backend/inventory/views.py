from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Publication, Unit, Package
from .serializers import PublicationSerializer, UnitSerializer, PackageSerializer

class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.filter(is_active=True)
    serializer_class = PublicationSerializer
    # Permiso: Cualquiera ve (GET), solo logueados editan
    permission_classes = [IsAuthenticatedOrReadOnly] 

    # AQUÍ VA TU LÓGICA DE RESTRICCIÓN
    def create(self, request, *args, **kwargs):
        # 1. Validar que sea Propietario
        if request.user.role != 'PROPIETARIO':
            return Response(
                {"error": "Acceso denegado. Debes cambiar a modo Host para publicar."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 2. Si pasa, dejamos que Django cree la publicación
        return super().create(request, *args, **kwargs)

    # Automatizar que el "owner" sea el usuario logueado
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# ... (Tu UnitViewSet sigue igual)
class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Igual que en Publicaciones, asignamos el dueño automáticamente
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)