from rest_framework import serializers
from api.models.Album import Album
from api.serializers.ArtistSerializer import ArtistSerializer

class AlbumSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)  # Nested Serializer

    class Meta:
        model = Album
        fields = "__all__"