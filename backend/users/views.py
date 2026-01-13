from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer

class UserViewSet(ModelViewSet):
    """
    Maneja todas las operaciones de usuarios (Crear, Leer, Actualizar).
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'firebase_uid' 
    
    # 1. SEGURIDAD DINÁMICA
    def get_permissions(self):
        """
        - Si la acción es 'create' (Registrarse): Permitimos entrar a cualquiera (AllowAny).
        - Para cualquier otra cosa (Ver perfil, Editar): Exigimos Token (IsAuthenticated).
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    # 2. LÓGICA DE CREACIÓN (Registro)
    def create(self, request, *args, **kwargs):
        firebase_uid = request.data.get('firebase_uid')

        if not firebase_uid:
            return Response(
                {'error': 'firebase_uid es obligatorio'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, created = CustomUser.objects.get_or_create(
            firebase_uid=firebase_uid,
            defaults={
                'username': firebase_uid, 
                'email': request.data.get('email', ''),
                'full_name': request.data.get('full_name', ''),
                'phone_number': request.data.get('phone_number', ''),
                'account_type': request.data.get('account_type', 'CLIENTE'), 
            }
        )

        serializer = self.get_serializer(user)
        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )