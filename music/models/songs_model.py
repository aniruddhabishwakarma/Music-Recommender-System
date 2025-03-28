from django.db import models

class Artist(models.Model):
    artist_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    link = models.URLField()
    picture_url = models.URLField()
    fans_count = models.IntegerField()

    def __str__(self):
        return self.name

class Album(models.Model):
    album_id = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    cover_url = models.URLField()
    release_date = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Song(models.Model):
    song_id = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=255)
    album = models.ForeignKey(
        'Album', 
        on_delete=models.SET_NULL,  # ✅ Allow NULL if album is deleted
        related_name="songs", 
        null=True, blank=True  # ✅ This allows the field to be NULL
    )
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name="songs")
    duration = models.IntegerField()
    preview_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
    

