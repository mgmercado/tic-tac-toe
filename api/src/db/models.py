from sqlalchemy.orm import relationship

from api.src.db.database import Base
from sqlalchemy import String, Column, Integer, CHAR, ForeignKey


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    symbol = Column(CHAR, nullable=False)

    games = relationship('Game', back_populates='players')

    def __repr__(self):
        return f"<Player name= {self.name} symbol={self.symbol}>"


class Game(Base):
    __tablename__ = 'game'
    game_id = Column(Integer, primary_key=True)
    players_id = Column(Integer, ForeignKey('player.id'))
    movements_played = Column(Integer, nullable=False)
    next_turn = Column(String(50))
    board = Column(String(50), nullable=False)
    winner = Column(String(50))

    players = relationship('Player', back_populates='games')
