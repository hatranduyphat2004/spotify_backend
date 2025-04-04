from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.models.Track import Track
from api.serializers.TrackSerializer import TrackSerializer

class TrackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            track = get_object_or_404(Track, pk=pk)
            serializer = TrackSerializer(track)
        else:
            tracks = Track.objects.all()
            serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        track = get_object_or_404(Track, pk=pk)
        serializer = TrackSerializer(track, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        track = get_object_or_404(Track, pk=pk)
        track.delete()
        return Response({"message": "Track deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
