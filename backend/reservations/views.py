from rest_framework import viewsets, permissions
from .models import Reserva
from .serializers import ReservaSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Si es Propietario, ve las reservas que le hicieron
        if user.rol.nombre == 'Propietario':
            return Reserva.objects.filter(propietario=user)
        # Si es Cliente, ve sus propias reservas (F-507)
        return Reserva.objects.filter(cliente=user)

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)