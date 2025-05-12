from rest_framework import serializers
from api.models.Lyric import Lyric


class LyricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyric
        fields = ['id', 'track', 'file_path']
