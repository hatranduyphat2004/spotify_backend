from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from api.serializers.ArtistSerializer import ArtistSerializer
from api.models.Artist import Artist


class ArtistView(APIView):
    permission_classes = [IsAuthenticated]  # Yêu cầu xác thực JWT
    parser_classes = (MultiPartParser, FormParser)  # Thêm hỗ trợ file upload

    def get(self, request, pk=None):
        """Lấy danh sách tất cả artists hoặc một artist cụ thể."""
        if pk:
            artist = get_object_or_404(Artist, pk=pk)
            serializer = ArtistSerializer(artist)
        else:
            artists = Artist.objects.all()
            serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Thêm một artist mới."""
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Cập nhật thông tin artist theo ID."""
        artist = get_object_or_404(Artist, pk=pk)
        serializer = ArtistSerializer(artist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Xoá artist theo ID."""
        artist = get_object_or_404(Artist, pk=pk)
        artist.delete()
        return Response({"message": "Artist deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
