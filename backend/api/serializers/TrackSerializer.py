from rest_framework import serializers
from api.models.Track import Track
from api.models.Artist import Artist

# Serializer cho Artist (chỉ chọn các trường cần thiết)


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['artist_id', 'name']  # hoặc thêm các trường khác nếu cần


class TrackSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        fields = '__all__'
