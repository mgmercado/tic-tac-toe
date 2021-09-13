from typing import Optional, List

from pydantic import BaseModel, Field

from api.src.entities.schemas import Player


class GameRequest(BaseModel):
    players: List[Player]
    starting_player: Optional[str] = None


class SubmitPlay(BaseModel):
    game_id: int
    player_name: str
    row: int = Field(gt=0, lt=4)
    column: int = Field(gt=0, lt=4)
