from rest_framework import serializers
from api.models.Playlist import Playlist
from .PlaylistTrackSerializer import PlaylistTrackSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = PlaylistTrackSerializer(source='playlist_tracks', many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'
