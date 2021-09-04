from sqlalchemy.orm import Session

from api.src.db import models
from api.src.db.database import Base
from api.src.entities import schemas
from pydantic import BaseModel


def get_player(db: Session, player_id: int):
    return _get_entity(db, models.Player, player_id)


def get_player_by_name(db: Session, name: str):
    return db.query(models.Player).filter(models.Player.name == name).first()


def get_players(db: Session, skip: int = 0, limit: int = 100):
    return _get_entities(db, models.Player, skip, limit)


def add_player(db: Session, new_player: schemas.Player):
    player_db = models.Player(
        name=new_player.name,
        symbol=new_player.symbol
    )
    db.add(player_db)
    db.commit()
    db.refresh(player_db)

    return player_db


def _get_entity(db: Session, model: Base, entity_id: int):
    return db.query(model).filter(model.id == entity_id).first()


def _get_entities(db: Session, model: Base, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()


def create_game(db: Session, new_game: schemas.Game):
    game_db = models.Player(**new_game.dict())
    db.add(game_db)
    db.commit()
    db.refresh(game_db)

    return game_db
