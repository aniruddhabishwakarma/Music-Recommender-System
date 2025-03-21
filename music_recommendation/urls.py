"""
URL configuration for music_recommendation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from music.views.songs_view import *
from music.views.user_view import *


urlpatterns = [
    path('', home, name='home'),
    path('album/<int:album_id>/', album_details, name='album-details'),
    path('artist/<int:artist_id>/', artist_details, name='artist-details'),  # ✅ Ensure this matches
    path('library/', library, name='library'),
    path('profile/', profile, name='profile'),
    path('admin/', admin.site.urls),
    path('api/search/', search_songs, name='search-songs'),
    path('search-results/', search_results_page, name='search-results'),
    path('api/song/<int:song_id>/', get_song_details, name='get-song-details'),
]