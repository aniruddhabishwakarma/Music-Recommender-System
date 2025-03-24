from django.db import models
from django.contrib.auth.models import User
from music.models.songs_model import Song, Artist

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_songs")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')

    def __str__(self):
        return f"{self.user.username} liked {self.song.title}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_artists")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="followers")
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artist')

    def __str__(self):
        return f"{self.user.username} follows {self.artist.name}"
