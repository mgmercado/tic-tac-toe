from typing import List, Optional

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from api.src.db.database import get_db
from api.src.entities.requests import GameRequest, SubmitPlay
from api.src.entities.schemas import Player, Game, PlayResponse
from api.src.services import game_service, player_service

router = APIRouter()


@router.get('/', status_code=200)
async def ping() -> dict:
    return {'message': 'pong!'}


@router.post('/new-game', response_model=Game)
async def new_game(game_request: GameRequest, db: Session = Depends(get_db)):
    return game_service.begin_game(db, game_request)


@router.get('/games', response_model=List[Game], status_code=200)
async def get_all_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        finished: Optional[bool] = None):
    return game_service.get_all_games(db, skip, limit, finished)


@router.get('/game/{game_id}')
async def get_game(game_id: int, db: Session = Depends(get_db)):
    return game_service.get_game(db, game_id)


@router.get('/players', response_model=List[Player], status_code=200)
async def get_all_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return player_service.get_all_players(db, skip, limit)


@router.get('/player/{player_id}')
async def get_player(player_id: int, db: Session = Depends(get_db)):
    return player_service.get_player(db, player_id)


@router.post('/player', response_model=Player, status_code=status.HTTP_201_CREATED)
async def create_player(player: Player, db: Session = Depends(get_db)):
    return player_service.add_player(db, player)


@router.post('/submit-play', response_model=Game, status_code=200)
async def submit_play(submit_play: SubmitPlay, db: Session = Depends(get_db)):
    return game_service.sumbit_play(db, submit_play)


@router.get('/game-movements/{game_id}', response_model=List[PlayResponse], status_code=200)
async def get_game_movements(game_id: int, db: Session = Depends(get_db)):
    return game_service.get_game_movements(db, game_id)
