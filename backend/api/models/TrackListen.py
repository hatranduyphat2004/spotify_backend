# api/models/TrackListen.py
from django.conf import settings
from django.db import models

from api.models.Track import Track


class TrackListen(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} listened to {self.track.title} at {self.listened_at}"
