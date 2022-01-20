from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.src.db.database import get_db
from api.src.entities.requests import GameRequest, SubmitPlay
from api.src.entities.schemas import Game, PlayResponse
from api.src.services.game_service import GameService

router = APIRouter(prefix='/game', tags=['Game'])


@router.post('/new', response_model=Game, status_code=201)
async def new_game(game_request: GameRequest, db: Session = Depends(get_db)):
    return GameService(db).begin_game(game_request)


@router.get('/all', response_model=List[Game], status_code=200)
async def get_all_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        finished: Optional[bool] = None):
    return GameService(db).get_all_games(skip, limit, finished)


@router.get('/{game_id}', response_model=Game, status_code=200)
async def get_game(game_id: int, db: Session = Depends(get_db)):
    return GameService(db).get_game(game_id)


@router.post('/submit-play', response_model=Game, status_code=201)
async def submit_play(move: SubmitPlay, db: Session = Depends(get_db)):
    return GameService(db).submit_play(move)


@router.get('/movements/{game_id}', response_model=List[PlayResponse], status_code=200)
async def get_game_movements(game_id: int, db: Session = Depends(get_db)):
    return GameService(db).get_game_movements(game_id)


@router.delete('/{game_id}', response_model=Game, status_code=200)
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    return GameService(db).delete_game(game_id)
