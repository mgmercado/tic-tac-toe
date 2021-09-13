from sqlalchemy import String, Column, Integer, CHAR, ForeignKey
from sqlalchemy.orm import relationship

from api.src.db.database import Base


class PlayerDB(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    symbol = Column(CHAR, nullable=False)
    game_id = Column(Integer, ForeignKey('game.id'))

    plays = relationship('PlayDB')


class GameDB(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    movements_played = Column(Integer, nullable=False)
    next_turn = Column(String(50))
    board = Column(String(255), nullable=False)
    winner = Column(String(50))

    players = relationship('PlayerDB')
    plays = relationship('PlayDB')


class PlayDB(Base):
    __tablename__ = 'play'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    player_id = Column(Integer, ForeignKey('player.id'))
    row = Column(Integer, nullable=False)
    column = Column(Integer, nullable=False)
