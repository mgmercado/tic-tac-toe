from typing import List

from api.src.entities.schemas import Player
from api.src.entities.requests import GameRequest


def begin_game(game_request: GameRequest) -> dict:
    players = _validate_symbol(game_request.players)
    next_turn = game_request.players[0].name
    board = [[None, None, None], [None, None, None], [None, None, None]]

    return {'game_id': 0, 'players': players, 'movements_played': 0, 'next_turn': next_turn, 'board': board}


def _validate_symbol(players: List[Player]) -> List[Player]:
    symbols = ('X', 'O')
    for player in players:
        player.symbol = symbols[players.index(player)] if not player.symbol else player.symbol

    return players
