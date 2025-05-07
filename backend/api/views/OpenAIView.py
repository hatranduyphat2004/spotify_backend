from openai import APIError, OpenAI
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import time
import logging

client = OpenAI(api_key=settings.OPENAI_API_KEY)
logger = logging.getLogger(__name__)

class ChatWithAIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get('message', '')

        if not user_message:
            return Response({
                "success": False,
                "message": "Trường 'message' là bắt buộc."
            }, status=status.HTTP_400_BAD_REQUEST)

        retries = 3
        backoff_factor = 2

        for attempt in range(retries):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Bạn là một trợ lý thông minh."},
                        {"role": "user", "content": user_message}
                    ]
                )
                reply = response.choices[0].message.content
                return Response({
                    "success": True,
                    "reply": reply
                }, status=status.HTTP_200_OK)

            except APIError as e:
                if "429" in str(e) and attempt < retries - 1:  # Xử lý giới hạn tốc độ
                    sleep_time = backoff_factor ** attempt
                    logger.warning(f"Vượt giới hạn tốc độ, thử lại sau {sleep_time} giây...")
                    time.sleep(sleep_time)
                    continue
                return Response({
                    "success": False,
                    "message": f"Lỗi từ OpenAI: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)