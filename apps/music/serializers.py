from rest_framework import serializers
from ..core.models import Music, ArtistProfile


class ArtistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistProfile
        fields = ['id']


class MusicSerializer(serializers.ModelSerializer):
    # artist = serializers.PrimaryKeyRelatedField(queryset=ArtistProfile.objects.all()) 
    artist = ArtistProfileSerializer(read_only=True)
    # artist = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Music
        fields = ["id", "title", "artist", "album_name", "genre", "created_at", "updated_at"]