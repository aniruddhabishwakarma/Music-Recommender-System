from django.db import models
from django.contrib.auth.models import User
from music.models.songs_model import Song, Artist

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_songs")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')
        db_table = 'music_like'

    def __str__(self):
        return f"{self.user.username} liked {self.song.title}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_artists")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="followers")
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artist')
        db_table = 'music_follow'

    def __str__(self):
        return f"{self.user.username} follows {self.artist.name}"

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'user')
        db_table = 'music_playlist'

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="songs")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('playlist', 'song')
        db_table = 'music_playlist_song'

    def __str__(self):
        return f"{self.song.title} in {self.playlist.name}"
