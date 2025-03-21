import requests
import time
from django.core.management.base import BaseCommand

# Deezer API Base URL
DEEZER_API_URL = "https://api.deezer.com"

# List of artists to check (Modify as needed)
ARTISTS_LIST = ["Porcupine Tree", "Arijit Singh", "Atif Aslam", "Ed Sheeran", "Ankit Tiwari"]

# Rate limit handling: 50 requests per 5 seconds
REQUEST_DELAY = 0.2  # 200ms between requests

def fetch_json(url):
    """Fetch JSON data from Deezer API with rate-limiting"""
    time.sleep(REQUEST_DELAY)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_artist_info(artist_name):
    """Fetch artist details and return artist ID"""
    url = f"{DEEZER_API_URL}/search/artist?q={artist_name}"
    data = fetch_json(url)

    if data and "data" in data and len(data["data"]) > 0:
        artist = data["data"][0]
        return artist["id"], artist["name"]
    return None, None

def get_artist_albums(artist_id):
    """Fetch all albums of an artist and return album count and album IDs"""
    url = f"{DEEZER_API_URL}/artist/{artist_id}/albums"
    data = fetch_json(url)

    albums = []
    if data and "data" in data:
        for album in data["data"]:
            albums.append(album["id"])  # Collect album IDs
    return albums

def get_album_tracks(album_id):
    """Fetch all tracks in an album and return song count"""
    url = f"{DEEZER_API_URL}/album/{album_id}/tracks"
    data = fetch_json(url)

    if data and "data" in data:
        return len(data["data"])  # Number of songs in the album
    return 0

class Command(BaseCommand):
    help = "Fetch artist, album, and song data from Deezer API"

    def handle(self, *args, **kwargs):
        for artist_name in ARTISTS_LIST:
            # Step 1: Get Artist Info
            artist_id, artist_real_name = get_artist_info(artist_name)
            if not artist_id:
                self.stdout.write(self.style.ERROR(f"❌ Artist {artist_name} not found."))
                continue

            # Step 2: Get All Albums
            album_ids = get_artist_albums(artist_id)
            num_albums = len(album_ids)

            # Step 3: Get Total Songs from All Albums
            total_songs = sum(get_album_tracks(album_id) for album_id in album_ids)

            self.stdout.write(self.style.SUCCESS(f"🎵 Artist: {artist_real_name}"))
            self.stdout.write(f"   🎼 Total Albums: {num_albums}")
            self.stdout.write(f"   🎶 Total Songs: {total_songs}\n")
