import firebase_admin
from firebase_admin import auth, credentials
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
import os

User = get_user_model()

# Inicializamos Firebase una sola vez de forma segura
if not firebase_admin._apps:
    try:
        cred_path = os.path.join(settings.BASE_DIR, 'firebase_cred.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error inicializando Firebase: {e}")

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # 1. Obtener el header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None 

        # 2. Validar formato "Bearer <TOKEN>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None 

        token = parts[1]

        try:
            # 3. Verificar el token con Firebase
            decoded_token = auth.verify_id_token(token, clock_skew_seconds=10)
            uid = decoded_token['uid']
        except Exception as e:
            # Si el token es inválido, expirado o falso, aquí cortamos el acceso.
            raise exceptions.AuthenticationFailed(f'Token inválido: {e}')

        try:
            # 4. Intentar buscar al usuario en la BD Postgres
            user = User.objects.get(username=uid)
            return (user, None)
            
        except User.DoesNotExist:
            
            return None