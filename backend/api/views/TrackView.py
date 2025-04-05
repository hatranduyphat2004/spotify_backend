from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.serializers.TrackSerializer import TrackSerializer
from api.models.Track import Track
from mutagen.mp3 import MP3


class TrackView(APIView):
    permission_classes = [IsAuthenticated]  # Yêu cầu xác thực JWT

    def get(self, request, pk=None):
        """Lấy danh sách tất cả tracks hoặc một track cụ thể."""
        if pk:
            track = get_object_or_404(Track, pk=pk)
            serializer = TrackSerializer(track)
        else:
            tracks = Track.objects.all()
            serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Thêm một track mới và tải file lên S3."""
        # Kiểm tra và lấy file nhạc từ request
        track_file = request.FILES.get('file_path')
        if not track_file:
            return Response({"error": "File nhạc không được để trống."}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo track mới từ dữ liệu request
        data = request.data
        data['file_path'] = track_file  # Thêm file vào request data

        serializer = TrackSerializer(data=data)
        if serializer.is_valid():
            # Lưu track vào cơ sở dữ liệu, bao gồm file tải lên S3
            track = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Cập nhật thông tin track theo ID, bao gồm cập nhật file nhạc nếu có."""
        track = get_object_or_404(Track, pk=pk)

        # Nếu có file mới được gửi trong request
        if 'file_path' in request.FILES:
            request.data['file_path'] = request.FILES['file_path']

        serializer = TrackSerializer(track, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Xoá track theo ID."""
        track = get_object_or_404(Track, pk=pk)
        track.delete()
        return Response({"message": "Track deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
