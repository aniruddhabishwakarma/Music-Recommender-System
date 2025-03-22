from django.contrib import admin
from django.urls import path
from music.views.songs_view import *
from music.views.user_view import *
from music.views.auth_view import * # ✅ Import properly
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('album/<int:album_id>/', album_details, name='album-details'),
    path('artist/<int:artist_id>/', artist_details, name='artist-details'),
    path('library/', library, name='library'),
    path('profile/', profile, name='profile'),
    path('admin/', admin.site.urls),
    path('api/search/', search_songs, name='search-songs'),
    path('search-results/', search_results_page, name='search-results'),
    path('api/song/<int:song_id>/', get_song_details, name='get-song-details'),
    
    # ✅ Use Custom Login & Registration Views
    path("login/", login_view, name="login"),  # ✅ Use our function-based login view
    path("logout/", logout_view, name="logout"),  # ✅ Logout Route
    path("register/", register_view, name="register"),  # ✅ Registration Route

    path('ajax/check-username/', check_username, name='check_username'),
    path('ajax/check-email/', check_email, name='check_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)