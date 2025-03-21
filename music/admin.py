from django.contrib import admin
from .models.songs_model import Artist, Album, Song

# Register your models here.

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
