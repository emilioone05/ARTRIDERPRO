from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'firebase_uid',
            'email',
            'full_name',
            'phone_number',
            'company_name',
            'location',
            'description',
            'account_type', 
        ]
        read_only_fields = ['id', 'firebase_uid'] 