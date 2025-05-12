from django.db import models
from .Folder import Folder
from .User import User
from .Track import Track


class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    folder = models.ForeignKey(
    Folder, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    cover_img_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def get_tracks(self):
        return Track.objects.filter(playlisttrack__playlist=self, playlisttrack__is_active=True)

    class Meta:
        db_table = 'playlist'

    def __str__(self):
        return f"Playlist {self.playlist_id}"
