from django.urls import path, include
from . import views

urlpatterns = [
    path('users/',views.UserListView.as_view(), name="user_list" ),
    path('users/<int:pk>/',views.UserDetailView.as_view(), name="user_detail" ),
    path('artists/',views.ArtistListView.as_view(), name="artist_list" ),
]