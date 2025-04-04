from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.models.Message import Message
from api.serializers.MessageSerializer import MessageSerializer

class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            message = get_object_or_404(Message, pk=pk)
            serializer = MessageSerializer(message)
        else:
            messages = Message.objects.all()
            serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return Response({"message": "Message deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
