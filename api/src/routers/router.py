from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from api.src.db.database import get_db
from api.src.entities.requests import GameRequest, SubmitPlay
from api.src.entities.schemas import Player, Game
from api.src.services import game_service, player_services

router = APIRouter()


@router.get('/', status_code=200)
async def ping() -> dict:
    return {'message': 'pong!'}


@router.post('/new-game', response_model=Game)
async def new_game(game_request: GameRequest, db: Session = Depends(get_db)):
    return game_service.begin_game(db, game_request)


@router.get('/players', response_model=List[Player], status_code=200)
async def get_all_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return player_services.get_all_players(db, skip, limit)


@router.get('/player/{player_id}')
async def get_player(player_id: int, db: Session = Depends(get_db)):
    return player_services.get_player(db, player_id)


@router.post('/player', response_model=Player, status_code=status.HTTP_201_CREATED)
async def create_player(player: Player, db: Session = Depends(get_db)):
    return player_services.add_player(db, player)


@router.put('/player/{player_id}')
async def update_player(player_id: int):
    pass


@router.delete('/player/{player_id}')
async def delete_player(player_id):
    pass


@router.post('/submit-play')
async def submit_play(submit_play: SubmitPlay, db: Session = Depends(get_db)):
    return game_service.sumbit_play(db, submit_play)
