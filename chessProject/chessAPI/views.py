import chess
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Game, Move
from .serializer import GameSerializer, MoveSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class MoveViewSet(viewsets.ModelViewSet):
    queryset = Move.objects.all()
    serializer_class = MoveSerializer

def makeMove(board, gameUCI):
    valid = False
    move = chess.Move.from_uci(gameUCI)
    if move in board.legal_moves:
        board.push(move)
        valid = True
    return valid

def getLegalMoves(board):
    moves = list(board.legal_moves)
    return [move.uci() for move in moves]

def isGameOver(board):
    return board.is_game_over()

def getGameResult(board):
    if board.is_checkmate():
        returnResult = "Checkmate"
    elif board.is_stalemate():
        returnResult = "Stalemate"
    elif board.is_insufficient_material():
        returnResult = "Insufficient material"
    elif board.is_seventyfive_moves():
        returnResult = "75-Move rule"
    elif board.is_fivefold_repetition():
        returnResult = "Five-fold repetition"
    else:
        returnResult = "Game in progress"
    
    return returnResult

@api_view(['POST'])
def makeMoveAPI(request):
    gameID = request.data.get('gameID')
    moveUCI = request.data.get('move')

    try:
        game = Game.objects.get(id=gameID)
    except Game.DoesNotExist:
        returnResponse = Response({'error' : 'Game with that ID not found'}, status = status.HTTP_404_NOT_FOUND)
    
    board = chess.Board(game.fen)
    
    if makeMove(board, moveUCI):
        game.fen = board.fen()
        game.save()

        Move.objects.create(game = game, uci = moveUCI)
        returnResponse = Response({
            'success' : True,
            'fen' : game.fen,
            'legalMoves' : getLegalMoves(board),
            'isGameOver' : isGameOver(board),
            'result' : getGameResult(board)
        })
    else:
        returnResponse = Response(
            {
            'success' : False,
            'error' : 'Invalid move'
            },
            status = status.HTTP_400_BAD_REQUEST)
    
    return returnResponse

@api_view(['GET'])
def getGameState(request, gameID):
    try:
        game = Game.objects.get(id = gameID)
    except Game.DoesNotExist:
        returnResponse = Response({'error' : 'Game with that ID not found'},
                                  status = status.HTTP_404_NOT_FOUND)
    board = chess.Board(game.fen)
    returnResponse = Response({
        'fen' : game.fen,
        'legalMoves' : getLegalMoves(board),
        'isGameOver' : isGameOver(board),
        'result' : getGameResult(board)
    })

    return returnResponse