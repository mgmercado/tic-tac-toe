from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.src.db import settings

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{server}:{port}/{db}".format(user=settings.USER,
                                                                                                password=settings.PASSWORD,
                                                                                                server=settings.SERVER,
                                                                                                port=settings.PORT,
                                                                                                db=settings.DATABASE)

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
