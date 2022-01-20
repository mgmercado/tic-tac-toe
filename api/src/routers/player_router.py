from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from api.src.db.database import get_db
from api.src.entities.schemas import Player
from api.src.services.player_service import PlayerService

router = APIRouter(prefix='/player', tags=['Player'])


@router.get('/all', response_model=List[Player], status_code=200)
async def get_all_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return PlayerService(db).get_all_players(skip, limit)


@router.get('/{player_id}')
async def get_player(player_id: int, db: Session = Depends(get_db)):
    return PlayerService(db).get_player(player_id)


@router.post('/add', response_model=Player, status_code=status.HTTP_201_CREATED)
async def create_player(player: Player, db: Session = Depends(get_db)):
    return PlayerService(db).add_player(player)
