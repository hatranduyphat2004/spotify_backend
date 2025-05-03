from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.serializers.TrackSerializer import TrackSerializer
from api.models.Track import Track
from api.models.ArtistTrack import ArtistTrack
from api.models.Artist import Artist

from mutagen.mp3 import MP3
from mutagen import MutagenError
import tempfile


class TrackView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

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
        # Kiểm tra các trường bắt buộc
        required_fields = ['title', 'artist_id']
        for field in required_fields:
            if field not in request.data:
                return Response({
                    "success": False,
                    "message": f"Thiếu trường bắt buộc: {field}"
                }, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra file nhạc
        track_file = request.FILES.get('file_path')
        if not track_file:
            return Response({
                "success": False,
                "message": "File nhạc không được để trống."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra artist tồn tại
        try:
            artist = Artist.objects.get(pk=request.data['artist_id'])
        except Artist.DoesNotExist:
            return Response({
                "success": False,
                "message": "Artist không tồn tại."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Chuẩn bị dữ liệu
        data = request.data
        data['file_path'] = track_file

        # Xử lý album
        if 'album' in data and data['album'] == 'none':
            data['album'] = None

        # Xử lý duration
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                for chunk in track_file.chunks():
                    temp_file.write(chunk)
                temp_file.flush()

                audio = MP3(temp_file.name)
                duration_seconds = int(audio.info.length)
                data['duration'] = duration_seconds

        except MutagenError:
            return Response({
                "success": False,
                "message": "Không thể phân tích file mp3. File có thể bị lỗi."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Lỗi khi xử lý file mp3: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Xử lý track_number
        if 'track_number' in data:
            if data['track_number'] is not None and data['track_number'] != 'null':
                try:
                    data['track_number'] = int(data['track_number'])
                except (ValueError, TypeError):
                    return Response({
                        "success": False,
                        "message": "Track number phải là số nguyên dương"
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                data['track_number'] = None
        else:
            data['track_number'] = None

        # Xử lý popularity
        if 'popularity' in data:
            try:
                data['popularity'] = int(data['popularity'])
            except (ValueError, TypeError):
                return Response({
                    "success": False,
                    "message": "Popularity phải là số nguyên dương"
                }, status=status.HTTP_400_BAD_REQUEST)

        # Xử lý is_active
        if 'is_active' in data:
            data['is_active'] = bool(data['is_active'])

        serializer = TrackSerializer(data=data)
        if serializer.is_valid():
            track = serializer.save()

            # Tạo ArtistTrack
            ArtistTrack.objects.create(
                artist=artist,
                track=track,
                role='primary'  # Mặc định là nghệ sĩ chính
            )

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

        # Chuẩn bị dữ liệu
        data = request.data.copy()

        # Xử lý file nhạc nếu có
        if 'file_path' in request.FILES:
            data['file_path'] = request.FILES['file_path']

        # Xử lý album
        if 'album' in data and data['album'] == 'none':
            data['album'] = None

        # Xử lý duration nếu có
        if 'duration' in data:
            try:
                data['duration'] = int(data['duration'])
            except (ValueError, TypeError):
                return Response({
                    "success": False,
                    "message": "Duration phải là số nguyên"
                }, status=status.HTTP_400_BAD_REQUEST)

        # Xử lý track_number nếu có
        if 'track_number' in data:
            try:
                data['track_number'] = int(data['track_number'])
            except (ValueError, TypeError):
                return Response({
                    "success": False,
                    "message": "Track number phải là số nguyên dương"
                }, status=status.HTTP_400_BAD_REQUEST)

        # Xử lý popularity nếu có
        if 'popularity' in data:
            try:
                data['popularity'] = int(data['popularity'])
            except (ValueError, TypeError):
                return Response({
                    "success": False,
                    "message": "Popularity phải là số nguyên dương"
                }, status=status.HTTP_400_BAD_REQUEST)

        # Xử lý is_active nếu có
        if 'is_active' in data:
            data['is_active'] = bool(data['is_active'])

        serializer = TrackSerializer(track, data=data, partial=True)
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
