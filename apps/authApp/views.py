from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from .utils import generate_access_token, generate_refresh_token, decode_jwt  
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]  #ensure JWTauthentication doesnot intercept

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]   #ensure JWTauthentication doesnot intercept

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)

            if user:
                access_token = generate_access_token(user)  # Generate access token
                refresh_token = generate_refresh_token(user)  # Generate refresh token
                return Response({
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "role": user.role
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Refresh the access token using a refresh token
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        user = decode_jwt(refresh_token)
        if user:
            # Issue a new access token
            access_token = generate_access_token(user)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
