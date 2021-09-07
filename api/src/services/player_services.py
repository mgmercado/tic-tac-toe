from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.src.db import crud
from api.src.entities.schemas import Player


def get_all_players(db: Session, skip: int = 0, limit: int = 100) -> List[Player]:
    return crud.get_players(db, skip, limit)


def get_player(db, player_id: int):
    player = crud.get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


def get_player_by_name(db, player_name: str):
    player = crud.get_player_by_name(db, player_name)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


def add_player(db: Session, new_player: Player):
    return crud.create_player(db, new_player)


def validate_symbol(players: List[Player]):
    symbols = ('X', 'O')
    for player in players:
        player.symbol = symbols[players.index(player)] if not player.symbol else player.symbol

    return players
