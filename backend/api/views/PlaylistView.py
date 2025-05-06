from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.Playlist import Playlist
from api.models.PlaylistTrack import PlaylistTrack
from api.models.Track import Track
from api.serializers.PlaylistSerializer import PlaylistSerializer


class PlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            playlist = get_object_or_404(Playlist, pk=pk)
            serializer = PlaylistSerializer(playlist)
        else:
            playlists = Playlist.objects.all()
            serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)
        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Xóa playlist
    def delete(self, request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)
        playlist.delete()
        return Response({"message": "Playlist deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    # Xóa track khỏi playlist
    def delete_track(self, request, playlist_id, track_id):
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        track = get_object_or_404(Track, pk=track_id)

        # Xóa PlaylistTrack liên quan
        playlist_track = get_object_or_404(PlaylistTrack, playlist=playlist, track=track)
        playlist_track.delete()

        return Response({
            "success": True,
            "message": "Track đã được xóa khỏi playlist."
        }, status=status.HTTP_204_NO_CONTENT)