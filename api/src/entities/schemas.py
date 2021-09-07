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
    board: str = '[[null, null, null], [null, null, null], [null, null, null]]'
    winner: Optional[str] = None

    class Config:
        orm_mode = True


class Play(BaseModel):
    game_id: int
    player_id: int
    row: int
    column: int

    class Config:
        orm_mode = True
