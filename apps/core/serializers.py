from rest_framework import serializers
from .models import User, ArtistProfile  # Assuming User is in the current app

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'phone', 'is_active', 'is_staff', 'created_at', 'updated_at']



class ArtistSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)  # Display user's email in the response
 
    class Meta:
        model = ArtistProfile
        fields = [
            'id', 'user_email', 'artist_name', 'dob', 'gender', 
            'address', 'first_release_year', 'no_of_albums_released', 
            'created_at', 'updated_at'
        ]