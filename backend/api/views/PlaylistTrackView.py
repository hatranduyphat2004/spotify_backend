from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.models.Playlist import Playlist
from api.models.Track import Track
from api.models.PlaylistTrack import PlaylistTrack
from api.serializers.PlaylistTrackSerializer import PlaylistTrackSerializer
from django.shortcuts import get_object_or_404

from api.serializers.TrackSerializer import TrackSerializer



class AddTrackToPlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, playlist_id):
        # Lấy playlist từ cơ sở dữ liệu
        playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)

        # Lấy tất cả các track của playlist thông qua PlaylistTrack
        playlist_tracks = PlaylistTrack.objects.filter(playlist=playlist).order_by('position')

        # Lấy danh sách track từ PlaylistTrack
        tracks = [playlist_track.track for playlist_track in playlist_tracks]

        # Serialize danh sách track
        serializer = TrackSerializer(tracks, many=True)

        return Response({
            "success": True,
            "message": "Lấy danh sách track thành công",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
        track_id = request.data.get('track_id')
        position = request.data.get('position', 0)

        if not track_id:
            return Response({
                "success": False,
                "message": "Thiếu track_id"
            }, status=status.HTTP_400_BAD_REQUEST)

        track = get_object_or_404(Track, pk=track_id)

        playlist_track = PlaylistTrack.objects.create(
            playlist=playlist,
            track=track,
            position=position
        )

        serializer = PlaylistTrackSerializer(playlist_track)
        return Response({
            "success": True,
            "message": "Đã thêm track vào playlist",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, playlist_id, track_id):
        # Lấy playlist và track từ cơ sở dữ liệu
        playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
        track = get_object_or_404(Track, pk=track_id)

        # Lấy PlaylistTrack liên kết với playlist và track này
        playlist_track = get_object_or_404(PlaylistTrack, playlist=playlist, track=track)

        # Xóa PlaylistTrack
        playlist_track.delete()

        return Response({
            "success": True,
            "message": "Track đã được xoá khỏi playlist thành công"
        }, status=status.HTTP_204_NO_CONTENT)