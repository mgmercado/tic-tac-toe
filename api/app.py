"""Main file with FastAPI setup."""
import uvicorn
from fastapi import FastAPI
from api.src.db import database
from api.src.db.models import Base
from api.src.routers import game_router, player_router, default_router

app = FastAPI(title='Tic-Tac-Toe')

app.include_router(game_router.router)
app.include_router(player_router.router)
app.include_router(default_router.router)
Base.metadata.drop_all(bind=database.engine)
Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=True)
