from rest_framework import serializers
from api.models.TrackListen import TrackListen

class TrackListenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackListen
        fields = ['user', 'track', 'listened_at']
