from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.serializers.TrackSerializer import TrackSerializer
from api.models.Track import Track


class TrackView(APIView):

    def get_permissions(self):
        """Chỉ yêu cầu xác thực cho các phương thức POST, PUT, DELETE"""
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated()]
        return []  # Không yêu cầu xác thực cho phương thức GET

    def get(self, request, pk=None):
        """Lấy danh sách tất cả tracks hoặc một track cụ thể."""
        if pk:
            track = get_object_or_404(Track, pk=pk)
            serializer = TrackSerializer(track)
        else:
            tracks = Track.objects.all()
            serializer = TrackSerializer(tracks, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """Thêm một track mới và tải file lên S3."""
        track_file = request.FILES.get('file_path')
        if not track_file:
            return Response({
                "success": False,
                "message": "File nhạc không được để trống."
            }, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['file_path'] = track_file  # Thêm file vào request data

        serializer = TrackSerializer(data=data)
        if serializer.is_valid():
            track = serializer.save()
            return Response({
                "success": True,
                "message": "Track đã được tạo thành công",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Dữ liệu không hợp lệ",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Cập nhật thông tin track theo ID, bao gồm cập nhật file nhạc nếu có."""
        track = get_object_or_404(Track, pk=pk)

        if 'file_path' in request.FILES:
            request.data['file_path'] = request.FILES['file_path']

        serializer = TrackSerializer(track, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Track đã được cập nhật thành công",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Dữ liệu không hợp lệ",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Xoá track theo ID."""
        track = get_object_or_404(Track, pk=pk)
        track.delete()
        return Response({
            "success": True,
            "message": "Track đã được xóa thành công"
        }, status=status.HTTP_204_NO_CONTENT)
