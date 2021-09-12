from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.src.db.database import Base
from api.src.db.models import PlayerDB, GameDB, PlayDB
from api.src.entities.schemas import Player, Game, Play


def _get_entity(db: Session, model: Base, entity_id: int) -> Base:
    return db.query(model).filter(model.id == entity_id).first()


def _get_entities(db: Session, model: Base, skip: int, limit: int) -> List[Base]:
    return db.query(model).offset(skip).limit(limit).all()


def _create_entity(db: Session, new_entity: BaseModel, model: Base) -> Base:
    entity_db = model(**new_entity.dict())
    _add_commit(db, entity_db)

    return entity_db


def get_player(db: Session, player_id: int) -> PlayerDB:
    return _get_entity(db, PlayerDB, player_id)


def get_player_by_name(db: Session, name: str) -> PlayerDB:
    return db.query(PlayerDB).filter(PlayerDB.name == name).first()


def get_players(db: Session, skip: int = 0, limit: int = 100) -> List[PlayerDB]:
    return _get_entities(db, PlayerDB, skip, limit)


def create_player(db: Session, new_player: Player) -> PlayerDB:
    return _create_entity(db, new_player, PlayerDB)


def create_game(db: Session, new_game: Game) -> GameDB:
    new_game.players = [PlayerDB(**player.dict()) for player in new_game.players]
    return _create_entity(db, new_game, GameDB)


def create_play(db: Session, new_play: Play) -> PlayDB:
    return _create_entity(db, new_play, PlayDB)


def _add_commit(db: Session, entity_db: Base):
    db.add(entity_db)
    db.commit()


def get_games(db: Session, skip: int, limit: int) -> List[GameDB]:
    return _get_entities(db, GameDB, skip, limit)


def get_game(db: Session, game_id: int) -> GameDB:
    return _get_entity(db, GameDB, game_id)


def update_game(db: Session, updated_game: GameDB) -> GameDB:
    _add_commit(db, updated_game)

    return updated_game
