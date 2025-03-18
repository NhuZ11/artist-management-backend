from rest_framework import serializers
from .models import User, ArtistProfile  # Assuming User is in the current app

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'phone', 'is_active', 'created_at']



class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model= ArtistProfile
        fields = '__all__'
