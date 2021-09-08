import json
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.src.db import crud
from api.src.entities.requests import GameRequest, SubmitPlay
from api.src.entities.schemas import Game, Play, Player
from api.src.services import player_services


def get_all_games(db: Session, skip: int = 0, limit: int = 100) -> List[Game]:
    return crud.get_games(db, skip, limit)


def get_game(db, game_id: int):
    game = crud.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


def create_game(db: Session, new_game: Game):
    return crud.create_game(db, new_game)


def begin_game(db: Session, game_request: GameRequest) -> dict:
    players = player_services.validate_symbol(game_request.players)
    players_names = [player.name for player in players]
    next_turn = game_request.starting_player if game_request.starting_player \
                                                and game_request.starting_player in players_names else players_names[0]
    new_game = Game(**{'players': players, 'movements_played': 0, 'next_turn': next_turn})
    return create_game(db, new_game)


def sumbit_play(db: Session, submit_play: SubmitPlay) -> Game:
    game = get_game(db, submit_play.game_id)
    player = player_services.get_player_by_name(db, submit_play.player_name)
    game.board = _board_play(game.board, player.symbol, submit_play.row, submit_play.column)
    game.movements_played += 1
    new_play = Play(**{'game_id': game.id,
                       'player_id': player.id,
                       'row': submit_play.row,
                       'column': submit_play.column})
    crud.create_play(db, new_play)
    crud.update_game(db, game)
    game.winner = _check_winner(game)
    return game


def _board_play(board: str, symbol: str, row: int, column: int) -> str:
    board = json.loads(board)
    board[row - 1][column - 1] = symbol
    return json.dumps(board)


def _check_winner(game: Game) -> Optional[str]:
    board = json.loads(game.board)
    flatboard = _flatten(board)

    for player in game.players:
        if flatboard[0] == flatboard[1] == flatboard[2] == player.symbol:
            return player.name
        if flatboard[0] == flatboard[3] == flatboard[6] == player.symbol:
            return player.name
        if flatboard[0] == flatboard[4] == flatboard[8] == player.symbol:
            return player.name
        if flatboard[1] == flatboard[4] == flatboard[7] == player.symbol:
            return player.name
        if flatboard[2] == flatboard[4] == flatboard[6] == player.symbol:
            return player.name
        if flatboard[2] == flatboard[5] == flatboard[8] == player.symbol:
            return player.name
        if flatboard[3] == flatboard[4] == flatboard[5] == player.symbol:
            return player.name
        if flatboard[6] == flatboard[7] == flatboard[8] == player.symbol:
            return player.name

    return None


def _flatten(nested_list: list) -> list:
    return [item for sublist in nested_list for item in sublist]
