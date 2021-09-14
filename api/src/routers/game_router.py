from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.src.db.database import get_db
from api.src.entities.requests import GameRequest, SubmitPlay
from api.src.entities.schemas import Game, PlayResponse
from api.src.services import game_service

router = APIRouter(prefix='/game', tags=['Game'])


@router.post('/new', response_model=Game, status_code=201)
async def new_game(game_request: GameRequest, db: Session = Depends(get_db)):
    return game_service.begin_game(db, game_request)


@router.get('/all', response_model=List[Game], status_code=200)
async def get_all_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        finished: Optional[bool] = None):
    return game_service.get_all_games(db, skip, limit, finished)


@router.get('/{game_id}', response_model=Game, status_code=200)
async def get_game(game_id: int, db: Session = Depends(get_db)):
    return game_service.get_game(db, game_id)


@router.post('/submit-play', response_model=Game, status_code=201)
async def submit_play(submit_play: SubmitPlay, db: Session = Depends(get_db)):
    return game_service.sumbit_play(db, submit_play)


@router.get('/movements/{game_id}', response_model=List[PlayResponse], status_code=200)
async def get_game_movements(game_id: int, db: Session = Depends(get_db)):
    return game_service.get_game_movements(db, game_id)


@router.delete('/{game_id}', response_model=Game, status_code=200)
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    return game_service.delete_game(db, game_id)
