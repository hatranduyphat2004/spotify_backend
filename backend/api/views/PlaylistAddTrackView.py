from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers.PlaylistTrackSerializer import PlaylistTrackSerializer

class PlaylistAddTrackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PlaylistTrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Track đã được thêm vào playlist.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Dữ liệu không hợp lệ.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
