# users/serializers.py
from rest_framework import serializers
from users.models import User

class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'profile_image', 'language', 'registered_at']

class UserMeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'profile_image', 'language']
