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
            # refresh = RefreshToken.for_user(user)
            return Response({
                  'user': UserSerializer(user).data,
                  # 'refresh': str(refresh),
                  # 'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
         
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def login(self, request):
      email = request.data.get('email')
      password = request.data.get('password')

      try:
         user = User.objects.get(email=email)  # Lấy user bằng email
      except User.DoesNotExist:
         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

      if user.check_password(password):  # Kiểm tra mật khẩu
         refresh = RefreshToken.for_user(user)
         return Response({
               'user': UserSerializer(user).data,
               'refresh': str(refresh),
               'access': str(refresh.access_token),
         }, status=status.HTTP_200_OK)

      return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


    def post(self, request, *args, **kwargs):
        action = kwargs.get('action')
        if action == 'register':
            return self.register(request)
        elif action == 'login':
            return self.login(request)
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
