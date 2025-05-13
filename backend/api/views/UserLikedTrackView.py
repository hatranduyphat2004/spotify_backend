from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.models.UserLikedTrack import UserLikedTrack
from api.serializers.UserLikedTrackSerializer import UserLikedTrackSerializer


class UserLikedTrackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            # Lọc theo user_id thay vì pk của UserLikedTrack
            liked_tracks = UserLikedTrack.objects.filter(
                user_id=pk, is_active=True)
            serializer = UserLikedTrackSerializer(liked_tracks, many=True)
        else:
            # Trả toàn bộ nếu không có pk
            liked_tracks = UserLikedTrack.objects.all()
            serializer = UserLikedTrackSerializer(liked_tracks, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserLikedTrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Cập nhật bản ghi UserLikedTrack theo ID (pk)
        """
        liked_track = get_object_or_404(UserLikedTrack, pk=pk)
        serializer = UserLikedTrackSerializer(
            liked_track, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, track_id):
        liked_track = get_object_or_404(
            UserLikedTrack, user_id=user_id, track_id=track_id
        )
        liked_track.delete()
        return Response({
            "success": True,
            "message": "Bỏ like thành công",
        }, status=status.HTTP_204_NO_CONTENT)
