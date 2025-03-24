from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from music.models.songs_model import *
from music.models.library_model import *

@login_required(login_url='/login/')
def like_toggle(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    like, created = Like.objects.get_or_create(user=request.user, song=song)

    if not created:
        like.delete()
        return JsonResponse({"liked": False, "message": "Song removed from favorites."})
    else:
        return JsonResponse({"liked": True, "message": "Song added to favorites!"})

# ✅ Toggle Follow
@login_required(login_url='/login/')
def follow_toggle(request, artist_id):
    artist = get_object_or_404(Artist, artist_id=artist_id)
    follow, created = Follow.objects.get_or_create(user=request.user, artist=artist)

    if not created:
        follow.delete()
        return JsonResponse({"following": False, "message": "You unfollowed the artist."})
    else:
        return JsonResponse({"following": True, "message": "You're now following this artist!"})