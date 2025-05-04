# message_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from api.models.Message import Message
from api.models.Conversation import Conversation
from api.models.ConversationMember import ConversationMember
from api.serializers.MessageSerializer import MessageSerializer

# Lấy lịch sử tin nhắn của một cuộc trò chuyện
class ConversationMessageHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        """Lấy lịch sử tin nhắn của cuộc trò chuyện"""
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id, is_active=True)
        messages = Message.objects.filter(conversation=conversation, is_active=True)
        message_serializer = MessageSerializer(messages, many=True)
        return Response({
                "success": True,
                "data": message_serializer.data
            }, status=status.HTTP_200_OK)

# Đánh dấu tin nhắn đã đọc
class MarkMessageAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, message_id):
        """Đánh dấu tin nhắn đã đọc"""
        message = get_object_or_404(Message, message_id=message_id)
        message.is_read = True
        message.save()
        return Response({"message": "Message marked as read"}, status=status.HTTP_200_OK)
    
# Gửi tin nhắn mới
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        """Gửi một tin nhắn mới trong cuộc trò chuyện"""
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id, is_active=True)
        
        message_content = request.data.get("message")
        if not message_content:
            return Response({"error": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # (Tuỳ chọn) Kiểm tra xem user có phải là thành viên của conversation không
        if not ConversationMember.objects.filter(conversation=conversation, user=request.user).exists():
            return Response({"error": "You are not a member of this conversation."}, status=status.HTTP_403_FORBIDDEN)

        # Gán sender là request.user (User model)
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=message_content,
            is_active=True
        )

        message_serializer = MessageSerializer(message)
        return Response({
                "success": True,
                "data": message_serializer.data
            }, status=status.HTTP_200_OK)



# Xoá tin nhắn
class DeleteMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, message_id):
        """Xoá tin nhắn"""
        message = get_object_or_404(Message, message_id=message_id)
        message.is_active = False
        message.save()
        return Response({"message": "Message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
