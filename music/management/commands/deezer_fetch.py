import requests
import time
from django.core.management.base import BaseCommand
from music.models import Artist, Album, Song  # Import your models

# Deezer API Base URL
DEEZER_API_URL = "https://api.deezer.com"

# List of artists to fetch (Modify as needed)
ARTISTS_LIST = ["Sonu Nigam", "Kuma Sagar", "Sajjan Raj Vaidya", "Durgesh Thapa", "Sushant Kc"]

# Rate limit handling: 50 requests per 5 seconds
REQUEST_DELAY = 0.2 # 200ms between requests

def fetch_json(url):
    """Fetch JSON data from Deezer API with rate-limiting"""
    time.sleep(REQUEST_DELAY)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_artist_info(artist_name):
    """Fetch artist details and return artist data"""
    url = f"{DEEZER_API_URL}/search/artist?q={artist_name}"
    data = fetch_json(url)

    if data and "data" in data and len(data["data"]) > 0:
        artist = data["data"][0]
        return {
            "artist_id": artist["id"],
            "name": artist["name"],
            "link": artist["link"],
            "picture_url": artist["picture_medium"],
            "fans_count": artist["nb_fan"]
        }
    return None

def get_artist_albums(artist_id):
    """Fetch all albums of an artist and return list of album data"""
    url = f"{DEEZER_API_URL}/artist/{artist_id}/albums"
    data = fetch_json(url)

    albums = []
    if data and "data" in data:
        for album in data["data"]:
            albums.append({
                "album_id": album["id"],
                "title": album["title"],
                "cover_url": album["cover_medium"],
                "release_date": album.get("release_date", "Unknown")
            })
    return albums

def get_album_tracks(album_id):
    """Fetch all tracks in an album and return list of song data"""
    url = f"{DEEZER_API_URL}/album/{album_id}/tracks"
    data = fetch_json(url)

    songs = []
    if data and "data" in data:
        for song in data["data"]:
            songs.append({
                "song_id": song["id"],
                "title": song["title"],
                "duration": song["duration"],
                "preview_url": song.get("preview", None)
            })
    return songs

class Command(BaseCommand):
    help = "Fetch and store artist, album, and song data from Deezer API"

    def handle(self, *args, **kwargs):
        for artist_name in ARTISTS_LIST:
            # Step 1: Get Artist Info
            artist_data = get_artist_info(artist_name)
            if not artist_data:
                self.stdout.write(self.style.ERROR(f"❌ Artist {artist_name} not found."))
                continue

            # Check if artist exists in DB, otherwise create
            artist, created = Artist.objects.get_or_create(
                artist_id=artist_data["artist_id"],
                defaults={
                    "name": artist_data["name"],
                    "link": artist_data["link"],
                    "picture_url": artist_data["picture_url"],
                    "fans_count": artist_data["fans_count"]
                }
            )

            # Step 2: Get Albums for the Artist
            album_data_list = get_artist_albums(artist.artist_id)
            for album_data in album_data_list:
                # Check if album exists, otherwise create
                album, created = Album.objects.get_or_create(
                    album_id=album_data["album_id"],
                    defaults={
                        "title": album_data["title"],
                        "artist": artist,
                        "cover_url": album_data["cover_url"],
                        "release_date": album_data["release_date"]
                    }
                )

                # Step 3: Get Songs for the Album
                song_data_list = get_album_tracks(album.album_id)
                for song_data in song_data_list:
                    # Check if song exists, otherwise create
                    Song.objects.get_or_create(
                        song_id=song_data["song_id"],
                        defaults={
                            "title": song_data["title"],
                            "album": album,
                            "artist": artist,
                            "duration": song_data["duration"],
                            "preview_url": song_data["preview_url"]
                        }
                    )

            self.stdout.write(self.style.SUCCESS(f"✅ {artist.name} - {len(album_data_list)} albums, {sum(len(get_album_tracks(a['album_id'])) for a in album_data_list)} songs stored."))
