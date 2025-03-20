from django.shortcuts import render
from django.db import connection
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from ..core.permissions import IsArtist
from .services import music_services
from .serializers import MusicSerializer
from ..core.models import ArtistProfile , Music

User = get_user_model()



# Create your views here.

class MusicListView(APIView):
    permission_classes = [IsAuthenticated, IsArtist]


    def get(self,request):
        email = request.user
        user = User.objects.get(email=email)
        artist = ArtistProfile.objects.get(user=user.id)
        musics = music_services.MusicManagerService.get_musics(artist.id)
        serializer = MusicSerializer(musics, many=True)
        return Response(serializer.data)
      


    def post(self, request):
        user = request.user
        try:
            artist = ArtistProfile.objects.get(user=user.id)
        except ArtistProfile.DoesNotExist:
            return Response({"error": "Artist profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            music_id = music_services.MusicManagerService.create_music(
                artist_id=artist.id,
                title=serializer.validated_data["title"],
                album_name=serializer.validated_data.get("album_name"),
                genre=serializer.validated_data.get("genre")
            )
            
            music = Music.objects.get(id=music_id)
            return Response(MusicSerializer(music).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicDetailView(APIView):
    permission_classes = [IsAuthenticated, IsArtist]

    def delete(self, request, pk):
        user = request.user

        try:
            artist = ArtistProfile.objects.get(user=user.id)
        except ArtistProfile.DoesNotExist:
            return Response({"error": "Artist profile not found"}, status=status.HTTP_404_NOT_FOUND)

        rows_deleted = music_services.MusicManagerService.delete_music(pk, artist.id)
        if rows_deleted == 0:
            return Response({"error": "Music not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": f"Rows deleted: {rows_deleted}"}, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        user = request.user
        try:
            artist = ArtistProfile.objects.get(user=user.id)
        except ArtistProfile.DoesNotExist:
            return Response({"error": "Artist profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            rows_updated = music_services.MusicManagerService.update_music(
                music_id=pk,
                artist_id=artist.id,
                title=serializer.validated_data["title"],
                album_name=serializer.validated_data.get("album_name"),
                genre=serializer.validated_data.get("genre")
            )
            if rows_updated == 0:
                return Response({"error": "Music not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": f"Rows updated: {rows_updated}"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)