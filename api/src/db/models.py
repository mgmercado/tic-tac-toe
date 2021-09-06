from sqlalchemy.orm import relationship

from api.src.db.database import Base
from sqlalchemy import String, Column, Integer, CHAR, ForeignKey


class PlayerDB(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    symbol = Column(CHAR, nullable=False)
    game_id = Column(Integer, ForeignKey('game.id'))

    def __repr__(self):
        return f"<Player name= {self.name} symbol={self.symbol}>"


class GameDB(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    movements_played = Column(Integer, nullable=False)
    next_turn = Column(String(50))
    board = Column(String(255), nullable=False)
    winner = Column(String(50))

    players = relationship('PlayerDB')
