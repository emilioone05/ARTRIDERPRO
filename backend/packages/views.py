from rest_framework import viewsets, permissions
from .models import Paquete
from .serializers import PaqueteSerializer

class PaqueteViewSet(viewsets.ModelViewSet):
    queryset = Paquete.objects.all()
    serializer_class = PaqueteSerializer
    permission_classes = [permissions.IsAuthenticated] # Solo usuarios logueados

    def perform_create(self, serializer):
        # Asigna automáticamente al usuario que crea el paquete como dueño
        serializer.save(propietario=self.request.user)

    def get_queryset(self):
        # Opcional: Si quieres que cada quien vea SOLO sus paquetes, descomenta esto:
        # return Paquete.objects.filter(propietario=self.request.user)
        return Paquete.objects.all() # Por ahora, todos ven todo (tipo Marketplace)