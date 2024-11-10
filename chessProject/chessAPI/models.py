from django.db import models

# Create your models here.
class Game(models.Model):
    fen = models.CharField(max_length=100,
                           default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='moves')
    uci = models.CharField(max_length=5)
    createdAt = models.DateTimeField(auto_now_add=True)