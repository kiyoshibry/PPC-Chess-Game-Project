from rest_framework import serializers
from .models import Game, Move

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'fen', 'createdAt', 'updatedAt']

class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ['id', 'game', 'uci', 'createdAt']