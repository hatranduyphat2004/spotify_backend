from rest_framework import serializers
from api.models.ArtistTrack import ArtistTrack

class ArtistTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistTrack
        fields = '__all__'
