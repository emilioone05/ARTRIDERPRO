from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .authentication import FirebaseAuthentication
from .serializers import UserProfileSerializer

class UpdateProfileView(APIView):
    # 1. Esto cumple el requisito de "Verificar Token"
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # El usuario ya fue identificado por el authentication_classes
        user = request.user 
        
        # 2. Esto cumple el requisito de "Recibir y Almacenar datos extra"
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Perfil completado exitosamente",
                "user_data": serializer.data
            })
        
        return Response(serializer.errors, status=400)