from django.db import models
from Album import Album

class Track(models.Model):
    track_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.IntegerField(help_text="Duration in seconds")
    file_path = models.CharField(max_length=500)
    track_number = models.PositiveIntegerField(null=True, blank=True)
    popularity = models.PositiveIntegerField(default=0)
    preview_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

