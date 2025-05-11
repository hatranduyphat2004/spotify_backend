from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.models.Lyric import Lyric
from api.models.Track import Track
from api.serializers.LyricSerializer import LyricSerializer


class GetLyricByTrackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, track_id):
        """Lấy lyric theo track_id."""
        track = get_object_or_404(Track, pk=track_id)
        lyric = get_object_or_404(Lyric, track=track)

        serializer = LyricSerializer(lyric)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
