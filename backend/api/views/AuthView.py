from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from ..serializers.UserSerializer import UserSerializer
from ..models.User import User


class AuthView(APIView):
    permission_classes = [AllowAny]

    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "success": True,
                "message": "Đăng kí thành công",
                "data": {
                    "user": UserSerializer(user).data
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Dữ liệu không hợp lệ",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            # Chỉ trả về thông báo lỗi chung
            return Response({
                "success": False,
                "message": "Email hoặc mật khẩu không đúng"
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "message": "Đăng nhập thành công",
            "data": {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        action = kwargs.get('action')
        if action == 'register':
            return self.register(request)
        elif action == 'login':
            return self.login(request)
        return Response({
            "success": False,
            "message": "Invalid action"
        }, status=status.HTTP_400_BAD_REQUEST)
