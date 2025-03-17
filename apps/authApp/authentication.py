#for authentication middleware
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None  # No token provided, can't authenticate

        try:
            token = auth_header.split(" ")[1]  # Extract token from 'Bearer <token>'
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            return (user, token)  # User object and token, if valid
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationFailed("Invalid or expired token.")
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found.")
