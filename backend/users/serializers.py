from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'phone', 'role', 'city')
        # Esto oculta la contraseña cuando pides los datos del usuario
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Usamos create_user para que hashee la contraseña (no guarde texto plano)
        user = User.objects.create_user(**validated_data)
        return user