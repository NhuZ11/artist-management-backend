from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'super_admin'

class IsArtistManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'artist_manager'

class IsArtist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'artist'


        
  