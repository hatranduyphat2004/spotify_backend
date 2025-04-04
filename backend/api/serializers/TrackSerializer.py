from rest_framework import serializers
from api.models.Track import Track

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'
