from django.core.management.base import BaseCommand
from music.models import Album, Song
from django.db.models import Count

class Command(BaseCommand):
    help = "Deletes albums that contain only one song but keeps the song"

    def handle(self, *args, **kwargs):
        # Get all albums that have only one song
        albums_to_delete = Album.objects.annotate(song_count=Count('songs')).filter(song_count=1)

        if not albums_to_delete.exists():
            self.stdout.write(self.style.SUCCESS("✅ No single-song albums found."))
            return

        deleted_count = 0

        for album in albums_to_delete:
            song = album.songs.first()  # Get the only song in this album
            if song:
                song.album = None  # ✅ Set album to NULL
                song.save()

            album.delete()  # Delete the album
            deleted_count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Deleted {deleted_count} albums and reassigned songs to have no album."))
