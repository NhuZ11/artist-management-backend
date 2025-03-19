from django.urls import path
from . import views

urlpatterns = [
    path('songs/', views.MusicListView.as_view(), name='song_list'),
    path('songs/<int:pk>/', views.MusicDetailView.as_view(), name='song_detail'),
]