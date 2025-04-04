from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.models.Folder import Folder
from api.serializers.FolderSerializer import FolderSerializer

class FolderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            folder = get_object_or_404(Folder, pk=pk)
            serializer = FolderSerializer(folder)
        else:
            folders = Folder.objects.all()
            serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        folder = get_object_or_404(Folder, pk=pk)
        serializer = FolderSerializer(folder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        folder = get_object_or_404(Folder, pk=pk)
        folder.delete()
        return Response({"message": "Folder deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
