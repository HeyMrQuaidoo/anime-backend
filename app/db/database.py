from contextlib import contextmanager
from sqlalchemy import DateTime, create_engine, orm, Column
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

SQLALCHAMY_DATABASE_URL = 'sqlite:///./app.db'

engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

class BaseMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__= {'always_refresh': True}

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    def to_dict(self, exclude = []):
        return dict([(k, getattr(self, k)) for k in self.__dict__.keys() if not k.startswith("_") and k not in exclude])

Base = declarative_base(cls=BaseMixin)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def SessionManager():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()