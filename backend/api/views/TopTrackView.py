from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.Track import Track
from api.serializers.TrackSerializer import TrackSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class TopTrackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Lấy tham số limit từ query params, mặc định là 10
        limit = request.query_params.get('limit', 10)

        try:
            limit = int(limit)
            if limit <= 0:
                raise ValueError()
        except ValueError:
            return Response({
                "success": False,
                "message": "Tham số 'limit' phải là số nguyên dương"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Lấy các track có popularity cao nhất
        top_tracks = Track.objects.order_by(
            '-created_at', '-popularity')[:limit]
        serializer = TrackSerializer(top_tracks, many=True)

        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
    def get_top_popular_tracks(self, request):
        try:
            # Lấy top 10 track phổ biến nhất
            top_10_tracks = Track.objects.order_by('-popularity', '-created_at')[:10]
            serializer_top_10 = TrackSerializer(top_10_tracks, many=True)
            for track in top_10_tracks:
                print(f"Track: {track.title}, Popularity: {track.popularity}, Created at: {track.created_at}")


            # Lấy top 50 track phổ biến nhất
            # top_50_tracks = Track.objects.order_by('-popularity', '-created_at')[:50]
            # serializer_top_50 = TrackSerializer(top_50_tracks, many=True)

            return Response({
                "success": True,
                "top_10": serializer_top_10.data,
                # "top_50": serializer_top_50.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, track_id):
        """
        Hàm này sẽ được gọi khi người dùng click vào bài hát, 
        tăng giá trị popularity lên 1 đơn vị.
        """
        try:
            # Lấy track bằng track_id
            track = Track.objects.get(id=track_id)
            
            # Tăng giá trị popularity lên 1
            track.popularity += 1
            track.save()

            # Trả về dữ liệu đã được cập nhật
            serializer = TrackSerializer(track)
            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        except Track.DoesNotExist:
            return Response({
                "success": False,
                "message": "Track không tồn tại"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
    