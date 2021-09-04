"""Main file with FastAPI setup."""

from fastapi import FastAPI
from api.src.routers import router

app = FastAPI()

app.include_router(router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
