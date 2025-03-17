from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from apps.core.models import ArtistProfile, ManagerProfile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1", "role"]
    
    def validate(self, data):
        if data["password"] != data["password1"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("password1")  
        
        role = validated_data.get("role", User.Role.ARTIST) 

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role=role
        )

        # Create profile based on role
        if role == User.Role.ARTIST:
            ArtistProfile.objects.create(user=user)
        elif role == User.Role.ARTIST_MANAGER:
            ManagerProfile.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
