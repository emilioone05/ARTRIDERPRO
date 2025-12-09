from rest_framework import serializers
from .models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
       
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'company_name', 'location', 
            'description'
        ]
        # El email y username vienen del firebase
        read_only_fields = ['email', 'username']