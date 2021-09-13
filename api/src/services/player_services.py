from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.src.db import crud
from api.src.entities.schemas import Player


def get_all_players(db: Session, skip: int = 0, limit: int = 100) -> List[Player]:
    """
    Returns all saved players from 0 to 100 by default
    :param db: database session
    :param skip: lower limit
    :param limit: max limit
    :return: list of players
    """
    return crud.get_players(db, skip, limit)


def get_player(db, player_id: int) -> Player:
    """
    Returns player with the requested id
    :param db: database session
    :param player_id: id of the game to find
    :return: found game
    :raises HTTPException: 404 Player not found
    """
    player = crud.get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


def get_player_by_name(db, player_name: str) -> Player:
    """
    Returns player the first player with the requested name
    :param db: database session
    :param player_name: name of the game to find
    :return: player found
    :raises HTTPException: 404 Player not found
    """
    player = crud.get_player_by_name(db, player_name)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


def add_player(db: Session, new_player: Player) -> Player:
    """
    Creates and stores a new player
    :param db: database session
    :param new_player: new player to store
    :return: stored new player
    """
    return crud.create_player(db, new_player)


def validate_symbol(players: List[Player]) -> List[Player]:
    """
    Assigns default players' symbols
    :param players: list of players
    :return: list of players with assigned symbols
    """
    symbols = ('X', 'O')
    for player in players:
        player.symbol = symbols[players.index(player)] if not player.symbol else player.symbol

    return players
