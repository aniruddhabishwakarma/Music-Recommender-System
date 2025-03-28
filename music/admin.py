from django.contrib import admin
from .models.songs_model import Artist, Album, Song
from .models.auth_model import *
from .models.library_model import *

# Register your models here.

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)

admin.site.register(Profile)
admin.site.register(SecurityQuestion)

admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Playlist)
admin.site.register(PlaylistSong)
admin.site.register(Review)