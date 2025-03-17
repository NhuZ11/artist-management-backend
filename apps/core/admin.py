from django.contrib import admin
from .models import User,ArtistProfile,ManagerProfile,Music

# Register your models here.
admin.site.register(User)
admin.site.register(ArtistProfile)
admin.site.register(ManagerProfile)
admin.site.register(Music)