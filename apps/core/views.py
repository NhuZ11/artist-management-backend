from django.views import View
from django.db import connection
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperAdmin, IsArtist, IsArtistManager
from .services import superadmin_services, artistmanager_service
from .serializers import UserSerializer, ArtistSerializer


class UserListView(APIView):
    permission_classes = [IsSuperAdmin]  # Ensure only authenticated users can access

    def get(self, request):
       users =  superadmin_services.SuperAdminServices.get_users()
       serializer = UserSerializer(users, many=True)
       return Response(serializer.data)
    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            role = serializer.validated_data.get("role")

            user_id = superadmin_services.SuperAdminServices.create_user(email,password,role)

            return Response({"message": "User created", "user_id": user_id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsSuperAdmin] 

    def get(self, request, pk):
        user = superadmin_services.SuperAdminServices.get_user_by_id(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk):
        rows_deleted = superadmin_services.SuperAdminServices.delete_user(pk)
        return Response(f"Rows deleted: {rows_deleted}", status=status.HTTP_200_OK)

    def patch(self, request, pk):
        new_password = request.data.get("password")
        new_role = request.data.get("role")
        updated_user = superadmin_services.SuperAdminServices.update_user(new_password,new_role,pk)
        serializer = UserSerializer(updated_user)
        return Response(serializer.data)
    

#Artist by artist_manager
class ArtistListCreateView(APIView):
    permission_classes=[IsArtistManager]

    def get(self, request):
       users =  artistmanager_service.ArtistManagerService.get_artists()
       serializer = ArtistSerializer(users, many=True)
       return Response(serializer.data)
    
    def post(self,request):
        serializer = ArtistSerializer(data=request.data)
        email= request.data.get("email")
        password = request.data.get("password")
        if serializer.is_valid():
            artist_name = serializer.validated_data.get("artist_name")

            
            artist_id = artistmanager_service.ArtistManagerService.create_artist_profile(artist_name,email,password)
            return Response({"message": "User created", "user_id": artist_id}, status=status.HTTP_201_CREATED)


class ArtistDetailView(APIView):
    permission_classes=[IsArtistManager]

    def delete(self,request,pk):
        rows_deleted = artistmanager_service.ArtistManagerService.delete_artist(pk)
        return Response(f"Rows deleted: {rows_deleted}", status=status.HTTP_200_OK)

    def patch(self, request, pk):
        artist_name = request.data.get("artist_name")
        dob = request.data.get("dob")
        gender = request.data.get("gender")
        address = request.data.get("address")
        first_release_year = request.data.get("first_release_year")
        no_of_albums_released = request.data.get("no_of_albums_released")

        updated_artist = artistmanager_service.ArtistManagerService.update_artist(
            artist_name, dob, gender, address, first_release_year, no_of_albums_released, pk
        )

        if updated_artist:
            serializer = ArtistSerializer(updated_artist)  # Now this gets a dictionary, not an int
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "Artist update failed or artist not found."}, status=400)