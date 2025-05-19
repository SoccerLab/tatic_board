from django.shortcuts import render, get_object_or_404

# boards/views.py
from rest_framework import generics, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Board, Scene, SceneObject, Team, Player, User 
from .serializers import (
    BoardListSerializer, BoardDetailSerializer,
    SceneObjectSerializer
)

class BoardView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BoardListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BoardListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        home = Team.objects.create(is_home=True, name="Home Team", color="blue")
        away = Team.objects.create(is_home=False, name="Away Team", color="red")
        board = Board.objects.create(
            owner=request.user,
            title=request.data['title'],
            match_type=request.data['match_type'],
            home_team=home,
            away_team=away,
        )
        if (board.match_type == "5:5"):
            num_of_players = 5
        elif (board.match_type == "6:6"):
            num_of_players = 6
        elif (board.match_type == "11:11"):
            num_of_players = 11
        else:
            num_of_players = 0
        scene = Scene.objects.create(board=board, order=1)
        for i in range(num_of_players):
            p1 = Player.objects.create(team=home, name="player", number=i)
            p2 = Player.objects.create(team=away, name="player", number=i)
            SceneObject.objects.create(scene=scene, player=p1, type="home", x=(i+0.1), y=(i+0.1))
            SceneObject.objects.create(scene=scene, player=p2, type="away", x=(2*i+0.1), y=(2*i+0.1))
        SceneObject.objects.create(scene=scene, type="ball", x=0.0, y=0.0)
        return Response(BoardDetailSerializer(board).data)

class BoardDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class BoardSaveView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, board_id):
        board = Board.objects.get(id=board_id, owner=request.user)
        data = request.data

        for team_type in ['home_team', 'away_team']:
            team_data = data.get(team_type)
            team = Team.objects.get(id=team_data['id'], board=board)
            team.name = team_data['name']
            team.color = team_data['color']
            team.save()

            # Update players
            Player.objects.filter(id__in=team_data.get('deleted_player_ids', [])).delete()
            for p in team_data['players']:
                player, _ = Player.objects.update_or_create(id=p['id'], defaults={
                    'team': team,
                    'name': p['name'],
                    'number': p['number'],
                    'position': p['position']
                })

        for s in data['scenes']:
            scene = Scene.objects.get(id=s['id'], board=board)
            scene.order = s['order']
            scene.save()
            SceneObject.objects.filter(id__in=s.get('deleted_object_ids', [])).delete()
            for o in s['objects']:
                SceneObject.objects.update_or_create(id=o['id'], defaults={
                    'scene': scene,
                    'player_id': o['player_id'],
                    'type': o['type'],
                    'x': o['x'],
                    'y': o['y']
                })

        return Response({'success': True})

class SceneObjectListView(generics.ListAPIView):
    serializer_class = SceneObjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        scene_id = self.kwargs['scene_id']
        return SceneObject.objects.filter(scene_id=scene_id)
    

# test views
class TestBoardView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BoardListSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']
        user = get_object_or_404(User, id=user_id)
        return Board.objects.filter(owner=user)

    def post(self, request, id):
        user = get_object_or_404(User, id=id)

        home = Team.objects.create(is_home=True, name="ManUtd", color="blue")
        away = Team.objects.create(is_home=False, name="Away Team", color="red")
        board = Board.objects.create(
            owner=user,
            title=request.data['title'],
            match_type=request.data['match_type'],
            layout="portrait",
            home_team=home,
            away_team=away,
        )

        if board.match_type == "5vs5":
            num_of_players = 5
        elif board.match_type == "6vs6":
            num_of_players = 6
        elif board.match_type == "11vs11":
            num_of_players = 11
        else:
            num_of_players = 0

        print(board)
        print(board.home_team)
        # s = Scene.objects.create(board=board, order=1)
        s = board.scenes.create(order=1)

        for i in range(num_of_players):
            p1 = Player.objects.create(team=home, name="player", number=i+1)
            p2 = Player.objects.create(team=away, name="player", number=i+1)
            SceneObject.objects.create(scene=s, player=p1, type="home", x=i + 0.1, y=i + 0.1)
            SceneObject.objects.create(scene=s, player=p2, type="away", x=2 * i + 0.1, y=2 * i + 0.1)

        SceneObject.objects.create(scene=s, type="ball", x=0.0, y=0.0)

        return Response(BoardDetailSerializer(board).data)
    
class TestBoardDetailView(APIView):
    permission_classes = [permissions.AllowAny]  # 또는 적절한 인증 설정

    def get(self, request, user_id, board_id):
        board = get_object_or_404(Board, id=board_id, owner=user_id)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, user_id, board_id):
        board = get_object_or_404(Board, id=board_id, owner=user_id)
        home = board.home_team
        away = board.away_team
        home.delete()
        away.delete()
        return Response({'detail': 'Board deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
class TestBoardSaveView(APIView):
    permission_classes = [permissions.AllowAny]  # 또는 적절한 인증 설정

    def post(self, request, user_id, board_id):
        data = request.data
        board = get_object_or_404(Board, id=board_id, owner=user_id)
        home_team = board.home_team
        away_team = board.away_team

        setattr(home_team, "name", data["home_team"]["name"])
        setattr(home_team, "color", data["home_team"]["color"])
        setattr(away_team, "name", data["away_team"]["name"])
        setattr(away_team, "color", data["away_team"]["color"])
        home_team.save()
        away_team.save()

        # 홈팀 삭제 선수
        Player.objects.filter(id__in=data['home_team'].get('deleted_player_ids', [])).delete()
        
        #홈팀
        for player_data in data["home_team"]['players']:
            if player_data.get('id') is None:
                Player.objects.create(team=home_team, **player_data)
            else:
                player = get_object_or_404(Player, id=player_data['id'], team=home_team)
                for attr, value in player_data.items():
                    setattr(player, attr, value)
                player.save()

        # 어웨이팀 삭제 선수
        Player.objects.filter(id__in=data['away_team'].get('deleted_player_ids', [])).delete()

        # 어웨이팀
        for player_data in data["away_team"]['players']:
            if player_data.get('id') is None:
                Player.objects.create(team=away_team, **player_data)
            else:
                player = get_object_or_404(Player, id=player_data['id'], team=away_team)
                for attr, value in player_data.items():
                    setattr(player, attr, value)
                player.save()


        # 씬
        Scene.objects.filter(id__in=data.get('deleted_scene_ids', [])).delete()
        for scene_data in data["scenes"]:
            if scene_data.get('id') is None:
                scene = Scene.objects.create(board=board, order=scene_data['order'])
            else:
                scene = get_object_or_404(Scene, id=scene_data['id'])

            # 씬 오브젝트
            SceneObject.objects.filter(id__in=scene_data.get('deleted_sceneobject_ids', [])).delete()
            for scene_object in scene_data['sceneobjects']:
                if scene_object.get('id') is None:
                    SceneObject.objects.create(scene=scene, **scene_object)
                else:
                    object = get_object_or_404(SceneObject, id=scene_object['id'])
                    for attr, value in scene_object.items():
                        setattr(object, attr, value)
                    object.save()

        return Response({"status": "success"})
    
class TestSceneObjectView(APIView):
    def get(self, request, scene_id):
        scene = get_object_or_404(Scene, id=scene_id)
        scene_objects = scene.sceneobjects.all()
        serializer = SceneObjectSerializer(scene_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)