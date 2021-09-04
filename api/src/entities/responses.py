from typing import List, Optional

from pydantic import BaseModel

from api.src.entities.schemas import Player


class GameResponse(BaseModel):
    game_id: str
    players: List[Player]
    movements_played: int
    next_turn: str
    board: List[list]
    winner: Optional[str] = None
