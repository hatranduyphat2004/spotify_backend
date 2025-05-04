
from django.urls import re_path
from api.consumer import ChatConsumer

# Định tuyến WebSocket cho các cuộc trò chuyện (chỉ định conversation_id trong URL)
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conversation_id>\d+)/$', ChatConsumer.as_asgi()),
]
