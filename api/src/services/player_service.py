from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.src.db.crud import Crud
from api.src.entities.schemas import Player
from api.src.services.service_interface import AppService


class PlayerService(AppService):
    def __init__(self, db: Session):
        super().__init__(db)
        self._crud = Crud(db)

    def get_all_players(self, skip: int = 0, limit: int = 100) -> List[Player]:
        """
        Returns all saved players from 0 to 100 by default
        :param skip: lower limit
        :param limit: max limit
        :return: list of players
        """
        return self._crud.get_players(skip, limit)

    def get_player(self, player_id: int) -> Player:
        """
        Returns player with the requested id
        :param player_id: id of the game to find
        :return: found game
        :raises HTTPException: 404 Player not found
        """
        player = self._crud.get_player(player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return player

    def get_player_by_name(self, player_name: str) -> Player:
        """
        Returns player the first player with the requested name
        :param player_name: name of the game to find
        :return: player found
        :raises HTTPException: 404 Player not found
        """
        player = self._crud.get_player_by_name(player_name)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return player

    def add_player(self, new_player: Player) -> Player:
        """
        Creates and stores a new player
        :param new_player: new player to store
        :return: stored new player
        """
        return self._crud.create_player(new_player)

    def validate_players(self, players: List[Player]):
        """
        Validates players being only 2 and having different names
        :param players: list of players
        :raises HTTPException: 406
        """
        if len(players) != 2:
            raise HTTPException(status_code=406, detail="Two players required")

        if players[0].name == players[1].name:
            raise HTTPException(status_code=406, detail="Players' names must be different")

    def validate_symbol(self, players: List[Player]) -> List[Player]:
        """
        Assigns default players' symbols and validates differences
        :param players: list of players
        :return: list of players with assigned symbols
        :raises HTTPException: 406
        """
        symbols = ('X', 'O')
        for player in players:
            player.symbol = symbols[players.index(player)] if not player.symbol else player.symbol

        if players[0].symbol.lower() == players[1].symbol.lower():
            raise HTTPException(status_code=406, detail="Players' symbols must be different")

        return players
