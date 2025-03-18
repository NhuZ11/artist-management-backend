from django.urls import path, include
from . import views

urlpatterns = [
    path('users/',views.UserListView.as_view(), name="user_list" ),
    path('users/<int:pk>/',views.UserDetailView.as_view(), name="user_detail" ),
    path('artists/',views.ArtistListCreateView.as_view(), name="artist_list" ),
    path('artists/<int:pk>/',views.ArtistDetailView.as_view(), name="artist_detail" ),
]