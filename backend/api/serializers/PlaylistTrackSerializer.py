from rest_framework import serializers
from api.models.PlaylistTrack import PlaylistTrack
from .TrackSerializer import TrackSerializer


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()

    class Meta:
        model = PlaylistTrack
        fields = '__all__'
