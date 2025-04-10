from rest_framework import serializers
from .models import Magaza
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MagazaSerializer(serializers.ModelSerializer):
    owner_details = UserSerializer(source='owner', read_only=True)
    
    class Meta:
        model = Magaza
        fields = ['id', 'ad', 'enlem', 'boylam', 'logo', 'location', 
                 'owner', 'owner_details', 'active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'owner']
