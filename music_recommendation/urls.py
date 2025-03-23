from django.contrib import admin
from django.urls import path
from music.views.songs_view import *
from music.views.user_view import *
from music.views.auth_view import *  # ✅ Import properly
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('album/<int:album_id>/', album_details, name='album-details'),
    path('profile/', profile, name='profile'),
    path('library/', library, name='library'),

    # ✅ Profile Update Views
    path('profile/update-info/', update_profile_info, name='update_profile_info'),
    path('profile/update-picture/', update_profile_picture, name='update_profile_picture'),
    path('profile/update-password/', update_password, name='update_password'),

    path('admin/', admin.site.urls),
    path('api/search/', search_songs, name='search-songs'),
    path('search-results/', search_results_page, name='search-results'),
    path('api/song/<int:song_id>/', get_song_details, name='get-song-details'),
    path("artist/<int:artist_id>/", artist_details, name="artist-details"),

    # ✅ Auth Views
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("set-security-question/", set_security_question, name="set_security_question"),

    # ✅ AJAX Checks
    path('ajax/check-username/', check_username, name='check_username'),
    path('ajax/check-email/', check_email, name='check_email'),

    # ✅ Forgot Password Flow
    path("forgot-password/", forgot_password_view, name="forgot_password"),
    path("forgot-password/verify/<str:username>/", verify_security_question_view, name="verify_security_question"),
    path("reset-password/", reset_password_confirm_view, name="reset_password"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)