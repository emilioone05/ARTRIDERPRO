from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Lógica de permisos:
    # - Cualquiera puede registrarse (POST create)
    # - Solo usuarios logueados pueden ver/editar perfiles
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    # --- LA MAGIA DEL UPGRADE A PROPIETARIO ---
    # Endpoint: POST /api/usuarios/upgrade_vendor/
    @action(detail=False, methods=['post'])
    def upgrade_vendor(self, request):
        user = request.user
        
        # Aquí validamos si ya es propietario para no repetir
        if user.role == 'PROPIETARIO':
            return Response({"message": "Ya eres propietario."}, status=200)

        # Hacemos el cambio de rol
        user.role = 'PROPIETARIO'
        # Opcional: user.is_verified = True (si confías ciegamente)
        user.save()
        
        return Response({
            "message": "¡Felicidades! Ahora tienes permisos de Propietario",
            "new_role": user.role
        })