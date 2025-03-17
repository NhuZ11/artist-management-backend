from django.views import View
from django.db import connection
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperAdmin, IsArtist
from .services import superadmin_services
from .serializers import UserSerializer


class UserListView(APIView):
    permission_classes = [IsSuperAdmin]  # Ensure only authenticated users can access

    def get(self, request):
       users =  superadmin_services.SuperAdminServices.get_users()
       serializer = UserSerializer(users, many=True)
       return Response(serializer.data)
    
    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")

        user_id = superadmin_services.SuperAdminServices.create_user(email,password,role)

        return Response({"message": "User created", "user_id": user_id}, status=status.HTTP_201_CREATED)
    

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