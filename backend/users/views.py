from django.shortcuts import render

# users/views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from users.models import User
from .serializers import UserMeSerializer, UserMeUpdateSerializer

class GoogleLoginAPIView(APIView):
    def post(self, request):
        token = request.data.get('id_token')
        print("login request!")
        if not token:
            return Response({'error': 'id_token is required'}, status=status.HTTP_400_BAD_REQUEST)
            print("token is not included")
        try:
            # 구글 토큰 검증
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)

            # idinfo에서 필요한 정보 추출
            email = idinfo.get('email')
            name = idinfo.get('name', '')
            picture = idinfo.get('picture', '')
            print(email)
            print(name)

            if not email:
                return Response({'error': 'Email not found in token'}, status=status.HTTP_400_BAD_REQUEST)

            # 유저 조회 또는 생성
            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email.split('@')[0],
                'name': name,
                'profile_image': picture,
            })
            
            print(user)

            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            print("refresh")
            print(refresh)
            response = Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                'user': {
                    'email': user.email,
                    'name': user.name,
                    'profile_image': user.profile_image,
                }
            })
            response.set_cookie(
                key='access',
                value=str(refresh.access_token),
                httponly=True,
                samesite='Lax',  # 'None' + Secure이면 크로스도메인도 가능
                secure=False,    # 개발 환경에서는 False, 배포시 True (HTTPS 필수)
                max_age=60 * 15  # access token 만료 시간 15분
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                samesite='Lax',
                secure=False,
                max_age=60 * 60 * 24 * 7  # 7일짜리 refresh token
            )
            return response

        except ValueError:
            print("invalid token")
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserMeView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserMeUpdateSerializer
        return UserMeSerializer

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'  # URL에서 user 식별
    lookup_url_kwarg = 'id'  # path('<int:id>/')와 매칭

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserMeUpdateSerializer
        return UserMeSerializer

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)