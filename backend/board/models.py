# boards/models.py
from django.db import models
from users.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    is_home = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Board(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=100)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_board")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_board")
    match_type = models.CharField(max_length=20) # 5:5 / 6:6 / 11:11 / null
    layout = models.CharField(max_length=20) # portrait / landscape
    thumbnail = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField() #등번호
    position = models.CharField(max_length=10)
    starter = models.BooleanField(null=True, blank=True) #if 스타팅맴버

    # # 팀 내에서 같은 등번호를 갖을 수 없음
    # class Meta:
    #     unique_together = ('team', 'number')

    def __str__(self):
        return f"{self.name} #{self.number}"

class Scene(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='scenes')
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"Scene {self.order} of Board {self.board.title}"

class SceneObject(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='sceneobjects')
    player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=10, choices=[("home", "Home"), ("away", "Away"), ("ball", "Ball")])
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return f"Object {self.player.name} in Scene {self.scene.order}"