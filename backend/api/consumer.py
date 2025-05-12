# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from api.models.Message import Message
from api.models.Conversation import Conversation
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user or self.user.is_anonymous:
            await self.close()
            return

        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get('message')

        user = self.scope["user"]
        conversation_id = self.conversation_id

        # Lưu message vào DB (chạy trong thread đồng bộ)
        message = await sync_to_async(Message.objects.create)(
            sender=user,
            conversation_id=conversation_id,
            content=content,
            sent_at=timezone.now()
        )
        # Broadcast cho các client trong group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content,
                'sender': user.id,
                'sender_username': user.username,
                'sent_at': str(message.sent_at),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_username': event['sender_username'],
            'sent_at': event['sent_at'],
        }))
