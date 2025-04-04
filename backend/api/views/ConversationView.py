from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.models.Conversation import Conversation
from api.serializers.ConversationSerializer import ConversationSerializer

class ConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            conversation = get_object_or_404(Conversation, pk=pk)
            serializer = ConversationSerializer(conversation)
        else:
            conversations = Conversation.objects.all()
            serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        serializer = ConversationSerializer(conversation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        conversation.delete()
        return Response({"message": "Conversation deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
