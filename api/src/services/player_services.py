from typing import List

from sqlalchemy.orm import Session

from api.src.db import models, crud
from api.src.db.database import SessionLocal
from api.src.entities.schemas import Player


# db = SessionLocal()


def get_all_players(db: Session, skip: int = 0, limit: int = 100) -> List[Player]:
    return crud.get_players(db, skip, limit)


def get_player(db, player_id: int):
    return crud.get_player(db, player_id)


def add_player(db: Session, new_player: Player):
    return crud.add_player(db, new_player)


def _validate_symbol(players: List[Player]):
    symbols = ('X', 'O')
    for player in players:
        player.symbol = symbols[players.index(player)] if not player.symbol else player.symbol

    return players
