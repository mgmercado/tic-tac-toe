from sqlalchemy.orm import Session


class DBSession:
    def __init__(self, db: Session):
        self._db = db


class AppService(DBSession):
    pass


class AppCRUD(DBSession):
    pass
