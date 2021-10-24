import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv('database.env')
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{server}:{port}/{db}".format(
    user=os.getenv('USER_DB'),
    password=os.getenv("PASSWORD"),
    server=os.getenv("SERVER"),
    port=os.getenv("PORT"),
    db=os.getenv("DATABASE"))

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
