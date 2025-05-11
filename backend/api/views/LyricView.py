from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from api.models.Lyric import Lyric
from api.serializers.LyricSerializer import LyricSerializer


class LyricView(APIView):
    permission_classes = [IsAuthenticated]  # Yêu cầu xác thực JWT

    def get(self, request, pk=None):
        """Lấy danh sách tất cả lyrics hoặc một lyric cụ thể theo ID."""
        if pk:
            lyric = get_object_or_404(Lyric, pk=pk)
            serializer = LyricSerializer(lyric)
            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            lyrics = Lyric.objects.all()
            serializer = LyricSerializer(lyrics, many=True)
            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

    def post(self, request):
        """Thêm lyric mới."""
        serializer = LyricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Lyric đã được tạo thành công",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Dữ liệu không hợp lệ",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Cập nhật lyric theo ID."""
        lyric = get_object_or_404(Lyric, pk=pk)
        serializer = LyricSerializer(lyric, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Lyric đã được cập nhật thành công",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "message": "Dữ liệu không hợp lệ",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Xoá lyric theo ID."""
        lyric = get_object_or_404(Lyric, pk=pk)
        lyric.delete()
        return Response({
            "success": True,
            "message": "Lyric đã được xoá thành công"
        }, status=status.HTTP_204_NO_CONTENT)
