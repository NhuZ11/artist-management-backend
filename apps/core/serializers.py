from rest_framework import serializers
from .models import User  # Assuming User is in the current app

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'phone', 'is_active', 'created_at']
