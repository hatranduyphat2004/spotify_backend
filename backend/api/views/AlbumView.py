from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from api.serializers.AlbumSerializer import AlbumSerializer
from api.models.Album import Album
from api.models.Artist import Artist
from api.models.ArtistAlbum import ArtistAlbum


class AlbumView(APIView):
    permission_classes = [IsAuthenticated]  # Yêu cầu xác thực JWT
    parser_classes = (MultiPartParser, FormParser)  # Hỗ trợ file upload

    def get(self, request, pk=None):
        """Lấy danh sách tất cả albums hoặc một album cụ thể."""
        if pk:
            album = get_object_or_404(Album, pk=pk)
            serializer = AlbumSerializer(album)
        else:
            albums = Album.objects.all()
            serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Thêm một album mới, yêu cầu có ít nhất một nghệ sĩ."""
        data = request.data.copy()  # Sử dụng copy() để đảm bảo dữ liệu có thể thay đổi
        # Lấy danh sách nghệ sĩ từ request
        artists_data = data.pop('artists', [])
        if not artists_data:
            return Response({"error": "Album phải thuộc ít nhất của một nghệ sĩ."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra album dữ liệu hợp lệ
        serializer = AlbumSerializer(data=data)
        if serializer.is_valid():
            album = serializer.save()

            # Lưu quan hệ giữa album và nghệ sĩ
            for artist_id in artists_data:
                artist = get_object_or_404(Artist, pk=artist_id)
                ArtistAlbum.objects.create(artist=artist, album=album)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors, "success": False}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Cập nhật thông tin album theo ID."""
        album = get_object_or_404(Album, pk=pk)
        serializer = AlbumSerializer(album, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Xoá album theo ID."""
        album = get_object_or_404(Album, pk=pk)
        album.delete()
        return Response({"message": "Album deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
