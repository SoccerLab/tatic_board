# boards/serializers.py
from rest_framework import serializers
from .models import Board, Team, Player, Scene, SceneObject

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'number', 'position']

class SceneObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneObject
        fields = ['id', 'player_id', 'type', 'x', 'y']

class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'color', 'players']

class SceneSerializer(serializers.ModelSerializer):
    sceneobjects = SceneObjectSerializer(many=True)

    class Meta:
        model = Scene
        fields = ['id', 'order', 'board', 'sceneobjects']

class SceneSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = ['id', 'order']

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'thumbnail', 'created_at', 'updated_at',]

class BoardDetailSerializer(serializers.ModelSerializer):
    home_team = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()
    scenes = SceneSimpleSerializer(many=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'home_team', 'away_team', 'scenes']

    def get_home_team(self, obj):
        team = obj.home_team
        return TeamSerializer(team).data if team else None

    def get_away_team(self, obj):
        team = obj.away_team
        return TeamSerializer(team).data if team else None