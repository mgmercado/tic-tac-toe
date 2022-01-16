import json
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.src.db import crud
from api.src.db.models import PlayerDB
from api.src.entities.requests import GameRequest, SubmitPlay
from api.src.entities.schemas import Game, Play, Player, PlayResponse
from api.src.services import player_service


def get_all_games(db: Session, skip: int = 0, limit: int = 100, finished: Optional[bool] = None) -> List[Game]:
    """
    Returns all saved games from 0 to 100 by default
    :param db: database session
    :param skip: lower limit
    :param limit: max limit
    :param finished: filter by finished games
    :return: list of games
    """
    return crud.get_games(db, skip, limit, finished)


def get_game(db: Session, game_id: int) -> Game:
    """
    Returns game with the requested id
    :param db: database session
    :param game_id: id of the game to find
    :return: game found
    :raises HTTPException: 404 Game not found
    """
    game = crud.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


def delete_game(db: Session, game_id: int) -> Game:
    """
    Delete a Game
    :param db: database session
    :param game_id: game id to be deleted
    :return: deleted game
    """
    game = get_game(db, game_id)
    return crud.delete_game(db, game)


def _create_game(db: Session, new_game: Game, finished: bool) -> Game:
    """
    Private function to store a new game
    :param db: database session
    :param new_game: new game to be stored
    :param finished: finished games
    :return: new game stored
    """
    return crud.create_game(db, new_game, finished)


def begin_game(db: Session, game_request: GameRequest) -> Game:
    """
    Set game's default attributes to begin a new game
    :param db: database session
    :param game_request: game request with players, symbols and starting player
    :return: new game stored
    """
    player_service.validate_players(game_request.players)
    players = player_service.validate_symbol(game_request.players)
    players_names = [player.name for player in players]
    next_turn = game_request.starting_player if game_request.starting_player \
                                                and game_request.starting_player in players_names else players_names[0]
    new_game = Game(**{'players': players,
                       'movements_played': 0,
                       'next_turn': next_turn})
    finished = False
    return _create_game(db, new_game, finished)


def sumbit_play(db: Session, submit_play: SubmitPlay) -> Game:
    """
    Creates a new play and updates current game being played
    :param db: database session
    :param submit_play: new play request
    :return: updated game stored
    """
    game = get_game(db, submit_play.game_id)
    _submit_play_validations(game, submit_play)
    player = player_service.get_player_by_name(db, submit_play.player_name)
    _new_play(db, game, submit_play, player)
    game.next_turn = _next_turn(game, player)

    finished = True if game.movements_played == 9 else False
    winner = _check_winner(game)
    if game.movements_played >= 5 and winner:
        game.winner = winner
        finished = True

    return crud.update_game(db, game, finished)


def _submit_play_validations(game: Game, submit_play: SubmitPlay):
    """
    Private function to validate current context before each movement is made
    :param game: current game
    :param submit_play: new play request
    :raises HTTPException: 406 with each case's message
    """
    if game.winner or game.movements_played == 9:
        raise HTTPException(status_code=406, detail="Game Finished")

    if game.next_turn != submit_play.player_name:
        raise HTTPException(status_code=406, detail="Not player's turn")

    board = json.loads(game.board)
    if board[submit_play.row - 1][submit_play.column - 1] is not None:
        raise HTTPException(status_code=406, detail="Movement already made")


def _board_play(board: str, symbol: str, row: int, column: int) -> str:
    """
    Private function to make a move in the board.
    :param board: saved board as str
    :param symbol: current symbol that makes the move
    :param row: row of the 3x3 board
    :param column: column of the 3x3 column
    :return: board in str format
    """
    board = json.loads(board)
    board[row - 1][column - 1] = symbol
    return json.dumps(board)


def _new_play(db: Session, game: Game, submit_play: SubmitPlay, player: PlayerDB):
    """
    Private function to creates and stores a new play and makes board movement
    :param db: database session
    :param game: current game
    :param submit_play: new play request
    :param player: current player making the move
    """
    game.board = _board_play(game.board, player.symbol, submit_play.row, submit_play.column)
    game.movements_played += 1
    new_play = Play(**{'game_id': game.id,
                       'player_id': player.id,
                       'row': submit_play.row,
                       'column': submit_play.column})
    crud.create_play(db, new_play)


def _next_turn(game: Game, player: Player) -> str:
    """
    Private function that decides who the next player is
    :param game: current game
    :param player: current player
    :return: next player's name
    """
    next_player = list(set(game.players) - {player})
    return next_player[0].name


def _check_winner(game: Game) -> Optional[str]:
    """
    Private function that checks if there is a winner
    :param game: current game
    :return: game's winner
    """
    board = json.loads(game.board)
    flatboard = _flatten(board)

    for player in game.players:
        if flatboard[0] == flatboard[1] == flatboard[2] == player.symbol or \
                flatboard[0] == flatboard[3] == flatboard[6] == player.symbol or \
                flatboard[0] == flatboard[4] == flatboard[8] == player.symbol or \
                flatboard[1] == flatboard[4] == flatboard[7] == player.symbol or \
                flatboard[2] == flatboard[4] == flatboard[6] == player.symbol or \
                flatboard[2] == flatboard[5] == flatboard[8] == player.symbol or \
                flatboard[3] == flatboard[4] == flatboard[5] == player.symbol or \
                flatboard[6] == flatboard[7] == flatboard[8] == player.symbol:
            return player.name

    return None


def _flatten(nested_list: list) -> list:
    """
    Private function to flat a nested list to one dimension list
    :param nested_list: list of lists
    :return: one dimension list
    """
    return [item for sublist in nested_list for item in sublist]


def get_game_movements(db: Session, game_id) -> List[PlayResponse]:
    """
    Returns a game's list of movements
    :param db: database session
    :param game_id: game the get movements
    :return: list of movements
    :raises HTTPException: 404 if game hase no movements yet
    """
    movements = crud.get_game_movements(db, game_id)
    if not movements:
        raise HTTPException(status_code=404, detail="No movements found for {}".format(game_id))

    for movement in movements:
        player = player_service.get_player(db, movement.player_id)
        movements[movements.index(movement)] = PlayResponse(game_id=movement.game_id,
                                                            player=player,
                                                            row=movement.row,
                                                            column=movement.column)

    return movements
