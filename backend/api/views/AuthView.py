from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from ..serializers.UserSerializer import UserSerializer
from ..models.User import User


class AuthView(APIView):
    permission_classes = [AllowAny]

    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserSerializer(user).data,
                'success': True,
                'message': "Đăng kí thành công",
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Dữ liệu không hợp lệ",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Thông tin đăng nhập không hợp lệ'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({
                'success': False,
                'message': 'Thông tin đăng nhập không hợp lệ'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'message': 'Đăng nhập thành công',
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        action = kwargs.get('action')
        if action == 'register':
            return self.register(request)
        elif action == 'login':
            return self.login(request)
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
