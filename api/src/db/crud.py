from typing import List, Optional

from pydantic import BaseModel

from api.src.db.database import Base
from api.src.db.models import PlayerDB, GameDB, PlayDB
from api.src.entities.schemas import Player, Game, Play
from api.src.services.service_interface import AppCRUD


class Crud(AppCRUD):

    def _get_entity(self, model: Base, entity_id: int) -> Base:
        """
        Private function to encapsulate get entity's logic
        :param db: database session
        :param model: database model to cast
        :param entity_id: entity's id to look
        :return: entity found
        """
        return self._db.query(model).filter(model.id == entity_id).first()

    def _get_entities(self, model: Base, skip: int, limit: int, filters=None) -> List[Base]:
        """
        Private function to encapsulate get entities' logic
        :param db: database session
        :param model: database model to cast
        :param skip: lower limit
        :param limit: max limit
        :param filters: filters to apply
        :return: list of entities
        """

        return self._db.query(model).filter(*filters).offset(skip).limit(limit).all()

    def _create_entity(self, new_entity: BaseModel, model: Base) -> Base:
        """
        Private function to encapsulate entities storage
        :param db: database session
        :param new_entity: new entity to store
        :param model: entity's model to cast
        :return: stored entity
        """
        entity_db = model(**new_entity.dict())
        self._add_commit(entity_db)

        return entity_db

    def get_player(self, player_id: int) -> PlayerDB:
        """
        Get player from database by id
        :param db: database session
        :param player_id: player's id to get
        :return: player found
        """
        return self._get_entity(PlayerDB, player_id)

    def get_player_by_name(self, name: str) -> PlayerDB:
        """
        Get player from database by name
        :param db: database session
        :param name: player's name to get
        :return: player found
        """
        return self._db.query(PlayerDB).filter(PlayerDB.name == name).first()

    def get_players(self, skip: int = 0, limit: int = 100) -> List[PlayerDB]:
        """
        Returns all saved players from 0 to 100 by default
        :param db: database session
        :param skip: lower limit
        :param limit: max limit
        :return: list of players
        """
        return self._get_entities(PlayerDB, skip, limit)

    def create_player(self, new_player: Player) -> PlayerDB:
        """
        Stores a new player
        :param db: database session
        :param new_player: new player to store
        :return: stored new player
        """
        return self._create_entity(new_player, PlayerDB)

    def create_game(self, new_game: Game, finished: bool) -> GameDB:
        """
        Stores a new game
        :param db: database session
        :param new_game: new game to store
        :param finished: finished games
        :return: stored new game
        """
        new_game.players = [self.get_player_by_name(player.name) if self.get_player_by_name(player.name)
                            else PlayerDB(**player.dict()) for player in new_game.players]
        new_game_db = GameDB(**new_game.dict(), finished=finished)
        self._add_commit(new_game_db)
        return new_game_db

    def create_play(self, new_play: Play) -> PlayDB:
        """
        Stores a new play
        :param db: database session
        :param new_play: new play to store
        :return: stored new play
        """
        return self._create_entity(new_play, PlayDB)

    def _add_commit(self, entity_db: Base):
        """
        Private function to encapsulate database add and commit
        :param db: database session
        :param entity_db: entity to be stored
        """
        self._db.add(entity_db)
        self._db.commit()

    def get_games(self, skip: int, limit: int, finished: Optional[bool] = None) -> List[GameDB]:
        """
        Returns all saved games from 0 to 100 by default
        :param db: database session
        :param skip: lower limit
        :param limit: max limit
        :return: list of games
        :param finished: to filter finished games
        """
        filters = [GameDB.finished == finished] if finished is not None else ()
        return self._get_entities(GameDB, skip, limit, filters)

    def get_game(self, game_id: int) -> GameDB:
        """
        Returns game with the requested id
        :param db: database session
        :param game_id: id of the game to find
        :return: game found
        """
        return self._get_entity(GameDB, game_id)

    def update_game(self, updated_game: GameDB, finished: bool) -> GameDB:
        """
        Updates an already stored game
        :param db: database session
        :param updated_game: game with new info
        :return: game with new info updated
        :param finished: finished game
        """
        updated_game.finished = finished
        self._add_commit(updated_game)

        return updated_game

    def get_game_movements(self, game_id: int) -> List[PlayDB]:
        """
        Returns a game's list of movements
        :param db: database session
        :param game_id: game the get movements
        :return: list of movements
        """
        return self._db.query(PlayDB).filter(PlayDB.game_id == game_id).all()

    def delete_game(self, game: Game) -> GameDB:
        """
        Delete a Game
        :param db: database session
        :param game: game to be deleted
        :return: deleted game
        """
        return self._delete_entity(game)

    def _delete_entity(self, entity: BaseModel) -> Base:
        """
        Private method to delete an entity
        :param db: database session
        :param entity: entity to be deleted
        :return: deleted entity
        """
        self._db.delete(entity)
        self._db.commit()
        return entity
