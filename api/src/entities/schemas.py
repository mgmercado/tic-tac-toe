from typing import Optional, List

from pydantic import BaseModel


class Player(BaseModel):
    name: str
    symbol: Optional[str] = None

    class Config:
        orm_mode = True


class Game(BaseModel):
    players: List[Player]
    movements_played: int
    next_turn: str
    board: str = '[[None, None, None], [None, None, None], [None, None, None]]'
    winner: Optional[str] = None

    class Config:
        orm_mode = True
