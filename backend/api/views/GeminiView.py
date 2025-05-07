import requests
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ChatWithGeminiAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get("message", "")
        if not user_message:
            return Response({
                "success": False,
                "message": "Trường 'message' là bắt buộc."
            }, status=status.HTTP_400_BAD_REQUEST)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{
                    "text": user_message
                }]
            }]
        }

        try:
            res = requests.post(url, headers=headers, data=json.dumps(payload))
            if res.ok:
                result = res.json()
                reply = result["candidates"][0]["content"]["parts"][0]["text"]
                return Response({
                    "success": True,
                    "message": "Phản hồi thành công",
                    "data": {
                        "reply": reply
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "message": f"Lỗi từ Gemini API: {res.status_code} - {res.text}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({
                "success": False,
                "message": f"Exception: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
