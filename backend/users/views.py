from django.shortcuts import render

# users/views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .serializers import UserMeSerializer, UserMeUpdateSerializer

class UserMeView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.AllowAny]

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