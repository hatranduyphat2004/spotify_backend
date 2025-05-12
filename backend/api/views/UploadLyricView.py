from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from api.models.Lyric import Lyric
from api.models.Track import Track
from api.serializers.LyricSerializer import LyricSerializer


class UploadLyricView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, track_id):
        track = get_object_or_404(Track, pk=track_id)
        file = request.FILES.get('file_path')

        if not file:
            return Response({
                "success": False,
                "message": "Vui lòng đính kèm file lyric (file_path)"
            }, status=status.HTTP_400_BAD_REQUEST)

        lyric, created = Lyric.objects.get_or_create(track=track)
        lyric.file_path = file
        lyric.save()

        serializer = LyricSerializer(lyric)
        return Response({
            "success": True,
            "message": "Lyric đã được {} thành công".format("tạo" if created else "cập nhật"),
            "data": serializer.data
        }, status=status.HTTP_200_OK)
