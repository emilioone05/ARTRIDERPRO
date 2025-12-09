from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None 

        token = auth_header.split(" ").pop()
        
        
        # MOCKUP:
        uid = "firebase_user_123" 
        email = "jeank_prueba@artrider.com"
        
        # Django busca si existe el usuario, si no, lo crea al vuelo
        user, created = User.objects.get_or_create(
            username=uid, 
            defaults={'email': email}
        )
        
        return (user, None)