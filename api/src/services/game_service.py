import json
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.src.db.crud import Crud
from api.src.db.models import PlayerDB
from api.src.entities.requests import GameRequest, SubmitPlay
from api.src.entities.schemas import Game, Play, Player, PlayResponse
from api.src.services.player_service import PlayerService
from api.src.services.service_interface import AppService


class GameService(AppService):
    def __init__(self, db: Session):
        super().__init__(db)
        self._crud = Crud(db)
        self.__player_service = PlayerService(db)

    def get_all_games(self, skip: int = 0, limit: int = 100, finished: Optional[bool] = None) -> List[
        Game]:
        """
        Returns all saved games from 0 to 100 by default
        :param skip: lower limit
        :param limit: max limit
        :param finished: filter by finished games
        :return: list of games
        """
        return self._crud.get_games(skip, limit, finished)

    def get_game(self, game_id: int) -> Game:
        """
        Returns game with the requested id
        :param game_id: id of the game to find
        :return: game found
        :raises HTTPException: 404 Game not found
        """
        game = self._crud.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game

    def delete_game(self, game_id: int) -> Game:
        """
        Delete a Game
        :param game_id: game id to be deleted
        :return: deleted game
        """
        game = self.get_game(game_id)
        return self._crud.delete_game(game)

    def _create_game(self, new_game: Game, finished: bool) -> Game:
        """
        Private function to store a new game
        :param new_game: new game to be stored
        :param finished: finished games
        :return: new game stored
        """
        return self._crud.create_game(new_game, finished)

    def begin_game(self, game_request: GameRequest) -> Game:
        """
        Set game's default attributes to begin a new game
        :param game_request: game request with players, symbols and starting player
        :return: new game stored
        """
        self.__player_service.validate_players(game_request.players)
        players = self.__player_service.validate_symbol(game_request.players)
        players_names = [player.name for player in players]
        next_turn = game_request.starting_player if game_request.starting_player \
                                                    and game_request.starting_player in players_names \
            else players_names[0]
        new_game = Game(**{'players': players,
                           'movements_played': 0,
                           'next_turn': next_turn})
        finished = False
        return self._create_game(new_game, finished)

    def submit_play(self, submit_play: SubmitPlay) -> Game:
        """
        Creates a new play and updates current game being played
        :param submit_play: new play request
        :return: updated game stored
        """
        game = self.get_game(submit_play.game_id)
        self._submit_play_validations(game, submit_play)
        player = self.__player_service.get_player_by_name(submit_play.player_name)
        self._new_play(game, submit_play, player)
        game.next_turn = self._next_turn(game, player)

        finished = True if game.movements_played == 9 else False
        winner = self._check_winner(game)
        if game.movements_played >= 5 and winner:
            game.winner = winner
            finished = True

        return self._crud.update_game(game, finished)

    def _submit_play_validations(self, game: Game, submit_play: SubmitPlay):
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

    def _board_play(self, board: str, symbol: str, row: int, column: int) -> str:
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

    def _new_play(self, game: Game, submit_play: SubmitPlay, player: PlayerDB):
        """
        Private function to creates and stores a new play and makes board movement
        :param game: current game
        :param submit_play: new play request
        :param player: current player making the move
        """
        game.board = self._board_play(game.board, player.symbol, submit_play.row, submit_play.column)
        game.movements_played += 1
        new_play = Play(**{'game_id': game.id,
                           'player_id': player.id,
                           'row': submit_play.row,
                           'column': submit_play.column})
        self._crud.create_play(new_play)

    def _next_turn(self, game: Game, player: Player) -> str:
        """
        Private function that decides who the next player is
        :param game: current game
        :param player: current player
        :return: next player's name
        """
        next_player = list(set(game.players) - {player})
        return next_player[0].name

    def _check_winner(self, game: Game) -> Optional[str]:
        """
        Private function that checks if there is a winner
        :param game: current game
        :return: game's winner
        """
        board = json.loads(game.board)
        flatboard = self._flatten(board)

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

    def _flatten(self, nested_list: list) -> list:
        """
        Private function to flat a nested list to one dimension list
        :param nested_list: list of lists
        :return: one dimension list
        """
        return [item for sublist in nested_list for item in sublist]

    def get_game_movements(self, game_id) -> List[PlayResponse]:
        """
        Returns a game's list of movements
        :param game_id: game the get movements
        :return: list of movements
        :raises HTTPException: 404 if game hase no movements yet
        """
        movements = self._crud.get_game_movements(game_id)
        if not movements:
            raise HTTPException(status_code=404, detail="No movements found for {}".format(game_id))

        for movement in movements:
            player = self.__player_service.get_player(movement.player_id)
            movements[movements.index(movement)] = PlayResponse(game_id=movement.game_id,
                                                                player=player,
                                                                row=movement.row,
                                                                column=movement.column)

        return movements
