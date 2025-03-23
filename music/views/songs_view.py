from django.shortcuts import render, get_object_or_404
from music.models.songs_model import Song, Artist, Album
import random
from django.http import JsonResponse
from fuzzywuzzy import process
from django.contrib.auth.decorators import login_required
import json

@login_required(login_url='/login/')
def home(request):
    query = request.GET.get('q', '')

    # ✅ Pop all toast flags from session
    show_login_toast = request.session.pop("login_success", False)
    show_logout_toast = request.session.pop("logout_success", False)
    show_security_toast = request.session.pop("security_question_set", False)

    if query:
        songs = Song.objects.filter(title__icontains=query) | Song.objects.filter(artist__name__icontains=query)
    else:
        songs = list(Song.objects.all().order_by('?')[:50])

    # ✅ Convert duration
    for song in songs:
        song.minutes = song.duration // 60
        song.seconds = song.duration % 60

    return render(request, 'music/home.html', {
        'songs': songs,
        'query': query,
        'show_login_toast': show_login_toast,
        'show_logout_toast': show_logout_toast,
        'show_security_toast': show_security_toast,
    })

@login_required(login_url='/login/')
def search_songs(request):
    """API endpoint for live searching with typo correction."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({"songs": [], "albums": [], "artists": [], "more_results": False}, safe=False)

    # Fetch all possible matches
    all_songs = list(Song.objects.all())
    all_albums = list(Album.objects.all())
    all_artists = list(Artist.objects.all())

    # Function to find the best match for a query using fuzzy matching
    def get_best_match(query, objects, field):
        from fuzzywuzzy import process
        choices = [getattr(obj, field) for obj in objects]
        best_match = process.extractOne(query, choices, score_cutoff=70)  # 70% similarity threshold
        if best_match:
            return [obj for obj in objects if getattr(obj, field) == best_match[0]]
        return []

    # Exact matches first
    exact_artist = list(Artist.objects.filter(name__iexact=query))
    exact_album = list(Album.objects.filter(title__iexact=query))
    exact_songs = list(Song.objects.filter(title__iexact=query))

    # Fuzzy matching (for typo corrections)
    fuzzy_artist = get_best_match(query, all_artists, "name") if not exact_artist else []
    fuzzy_album = get_best_match(query, all_albums, "title") if not exact_album else []
    fuzzy_songs = get_best_match(query, all_songs, "title") if not exact_songs else []

    # Combine results with correct priority:
    artists = exact_artist + fuzzy_artist
    albums = exact_album + fuzzy_album
    songs = exact_songs + fuzzy_songs

    # ✅ Fix: Use artist.artist_id instead of artist.id
    artist_list = [{
        "id": artist.artist_id,
        "name": artist.name,
        "cover_url": artist.picture_url,
        "type": "artist"
    } for artist in artists[:2]]

    album_list = [{
        "id": album.id,
        "title": album.title,
        "artist": album.artist.name,
        "cover_url": album.cover_url,
        "type": "album"
    } for album in albums[:2]]

    song_list = [{
        "id": song.id,
        "title": song.title,
        "artist": song.artist.name,
        "cover_url": song.album.cover_url if song.album else None,
        "type": "song"
    } for song in songs[:3]]

    more_results = len(artists) + len(albums) + len(songs) > 5

    return JsonResponse({
        "artists": artist_list,
        "albums": album_list,
        "songs": song_list,
        "more_results": more_results
    }, safe=False)

@login_required(login_url='/login/')
def search_results_page(request):
    """View to display full search results"""
    query = request.GET.get('q', '')
    songs = Song.objects.filter(title__icontains=query) | Song.objects.filter(artist__name__icontains=query) if query else []
    
    for song in songs:
        song.minutes = song.duration // 60
        song.seconds = song.duration % 60

    return render(request, 'music/search_results.html', {'songs': songs, 'query': query})


@login_required(login_url='/login/')
def album_details(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    songs = Song.objects.filter(album=album)

    songs_data = [
        {
            "title": song.title,
            "duration": song.duration or 0
        }
        for song in songs
    ]

    response = {
        "title": album.title,
        "cover": album.cover_url,
        "songs": songs_data
    }

    return JsonResponse(response)

@login_required(login_url='/login/')
def get_song_details(request, song_id):
    """API to fetch full song details for the modal"""
    
    song = get_object_or_404(Song, id=song_id)

    response_data = {
        "song_id": song.id,
        "title": song.title,
        "duration": song.duration,
        "minutes": song.duration // 60,
        "seconds": song.duration % 60,
        "preview_url": song.preview_url if song.preview_url else None,

        # ✅ Artist Details
        "artist": {
            "id": song.artist.id,
            "artist_id": song.artist.artist_id,  # ✅ ADD THIS LINE
            "name": song.artist.name,
            "picture_url": song.artist.picture_url,
            "link": song.artist.link,
            "fans_count": song.artist.fans_count
        },


        # ✅ Album Details
        "album": {
            "id": song.album.id if song.album else None,
            "title": song.album.title if song.album else "Unknown Album",
            "cover_url": song.album.cover_url if song.album else "/static/default_album.jpg",
            "release_date": song.album.release_date if song.album else "Unknown Release Date"
        }
    }

    return JsonResponse(response_data)

@login_required
def library(request):
    return render(request, "music/library.html")

@login_required(login_url='/login/')
def artist_details(request, artist_id):
    # ✅ Get the artist object
    artist = get_object_or_404(Artist, artist_id=artist_id)

    # ✅ Get 10 random songs for the artist
    songs = list(Song.objects.filter(artist=artist).order_by('?')[:10])
    for song in songs:
        song.minutes = song.duration // 60
        song.seconds = song.duration % 60

    # ✅ Get all albums of the artist
    albums = Album.objects.filter(artist=artist)

    # ✅ Add a JSON string of songs for each album
    for album in albums:
        album_songs = Song.objects.filter(album=album)
        album.songs_data = json.dumps([
            {
                "title": s.title,
                "duration": s.duration or 0
            }
            for s in album_songs
        ])

    # ✅ Render the artist details page
    return render(request, "music/artist_details.html", {
        "artist": artist,
        "songs": songs,
        "albums": albums
    })