from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.src.db import crud
from api.src.entities.requests import GameRequest
from api.src.entities.schemas import Player, Game

# db = SessionLocal()
from api.src.services import player_services


def get_all_games(db: Session, skip: int = 0, limit: int = 100) -> List[Game]:
    return crud.get_games(db, skip, limit)


def get_game(db, game_id: int):
    player = crud.get_game(db, game_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


def create_game(db: Session, new_game: Game):
    return crud.create_game(db, new_game)


def begin_game(db: Session, game_request: GameRequest) -> dict:
    players = player_services.validate_symbol(game_request.players)
    next_turn = players[0].name
    new_game = Game(**{'players': players, 'movements_played': 0, 'next_turn': next_turn})
    return create_game(db, new_game)
