from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from music.models.songs_model import *
from music.models.library_model import *
from django.http import JsonResponse
import json
from django.views.decorators.http import require_GET, require_POST

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
    

@require_POST
@login_required(login_url='/login/')
def create_playlist(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        song_id = data.get('song_id')

        if not name or not song_id:
            return JsonResponse({'success': False, 'message': 'Playlist name and song ID are required.'})

        # Check if playlist exists
        playlist, created = Playlist.objects.get_or_create(name=name, user=request.user)

        # Check if the song exists
        song = get_object_or_404(Song, id=song_id)

        # Add song to playlist if not already added
        playlist_song, added = PlaylistSong.objects.get_or_create(
            playlist=playlist, user=request.user, song=song
        )

        if not added:
            return JsonResponse({'success': False, 'message': 'Song already exists in the playlist.'})

        return JsonResponse({
            'success': True,
            'message': f'Song added to playlist "{playlist.name}".'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})



@login_required(login_url='/login/')
def add_to_playlist(request):
    try:
        data = json.loads(request.body)
        playlist_id = data.get('playlist_id')
        song_id = data.get('song_id')

        if not playlist_id or not song_id:
            return JsonResponse({'success': False, 'message': 'Missing playlist or song ID.'})

        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        song = get_object_or_404(Song, id=song_id)

        playlist_song, created = PlaylistSong.objects.get_or_create(
            playlist=playlist, user=request.user, song=song
        )

        if not created:
            return JsonResponse({'success': False, 'message': 'Song already in playlist.'})

        return JsonResponse({'success': True, 'message': 'Song added successfully to playlist.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    



@login_required(login_url='/login/')
def get_user_playlists(request):
    playlists = Playlist.objects.filter(user=request.user).order_by('-created_at')
    data = [
        {'id': p.id, 'name': p.name}
        for p in playlists
    ]
    return JsonResponse({'playlists': data})


@require_GET
def get_reviews(request, song_id):
    reviews = Review.objects.filter(song__id=song_id).select_related('user')
    data = [
        {
            'user': r.user.username,
            'content': r.content,
            'created_at': r.created_at.strftime("%b %d, %Y %I:%M %p")
        }
        for r in reviews
    ]
    return JsonResponse({'reviews': data})


@require_POST
@login_required(login_url='/login/')
def submit_review(request):
    try:
        data = json.loads(request.body)
        song_id = data.get('song_id')
        content = data.get('content')

        song = get_object_or_404(Song, id=song_id)
        review = Review.objects.create(user=request.user, song=song, content=content)
        print("🔥 Review submitted for song ID:", song_id)
        return JsonResponse({
            'success': True,
            'message': "Review added successfully.",
            'review': {
                'user': review.user.username,
                'content': review.content,
                'created_at': review.created_at.strftime("%b %d, %Y %I:%M %p")
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
def format_duration(seconds):
    minutes = seconds // 60
    remaining = seconds % 60
    return f"{minutes}m {remaining}s"

@login_required(login_url='/login/')
def library(request):
    liked_songs = Song.objects.filter(likes__user=request.user).select_related('artist', 'album')
    followed_artists = Artist.objects.filter(followers__user=request.user)
    playlists = Playlist.objects.filter(user=request.user).prefetch_related('songs__song__artist', 'songs__song__album')

    # Format duration for liked songs
    for song in liked_songs:
        song.duration_formatted = format_duration(song.duration)

    # Format duration for playlist songs
    for playlist in playlists:
        for ps in playlist.songs.all():
            ps.song.duration_formatted = format_duration(ps.song.duration)

    context = {
        'liked_songs': liked_songs,
        'followed_artists': followed_artists,
        'playlists': playlists,
    }
    return render(request, 'music/library.html', context)