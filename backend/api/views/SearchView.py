from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.Track import Track
from api.serializers.TrackSerializer import TrackSerializer
from rest_framework.permissions import IsAuthenticated


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '').strip()

        if not query:
            return Response({
                "success": True,
                "data": []
            }, status=status.HTTP_200_OK)

        tracks = Track.objects.filter(title__icontains=query, is_active=True)[
            :20]  # giới hạn 20 kết quả
        serializer = TrackSerializer(tracks, many=True)

        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
