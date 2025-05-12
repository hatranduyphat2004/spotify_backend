from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.Track import Track
from api.serializers.TrackSerializer import TrackSerializer


class IncreasePopularityView(APIView):
    def put(self, request, track_id):
        """
        Tăng popularity của một track theo ID.
        """
        try:
            track = Track.objects.get(track_id=track_id)
            track.popularity += 1
            track.save()
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
