from django.db import models
from .Track import Track


class Lyric(models.Model):
    track = models.OneToOneField(
        Track,
        on_delete=models.CASCADE,
        related_name='lyric'
    )
    file_path = models.FileField(upload_to='lyrics/', null=True, blank=True)

    class Meta:
        db_table = 'lyric'

    def __str__(self):
        return f"Lyrics for {self.track.title}"
