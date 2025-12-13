from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Rol

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'rol', 'company_name', 'location']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password) # Encriptar contraseña
        user.save()
        return user