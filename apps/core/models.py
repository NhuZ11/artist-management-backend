from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        ARTIST_MANAGER = "artist_manager", "Artist Manager"
        ARTIST = "artist", "Artist"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ARTIST)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager() #custom user manager

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="artist_profile")
    artist_name = models.CharField(max_length=200)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other')], blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    first_release_year = models.IntegerField(blank=True, null=True)
    no_of_albums_released = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manager_profile")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

class Music(models.Model):
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    album_name = models.CharField(max_length=255, blank=True, null=True)
    genre_choices = [('mb', 'Metal'), ('country', 'Country'), ('classic', 'Classic'), ('rock', 'Rock'), ('jazz', 'Jazz')]
    genre = models.CharField(max_length=20, choices=genre_choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Album(models.Model):
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    release_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title