from datetime import datetime
from sqlalchemy import Column, DateTime, String, JSON
from app.db.database import Base as Base

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True)
    email = Column(String, nullable=True)
    username = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    favorites = Column(JSON, nullable=True)
    last_login_time = Column(DateTime, nullable=True, default=datetime.now())

    def update_last_login_time(self):
        self.last_login_time = self.current_login_time
        self.current_login_time = datetime.now()

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}', username='{self.username}')"
    
    def to_dict(self, exclude=None):
        if exclude is None:
            exclude = set()
        data = {}
        for key in self.__dict__.keys():
            if not key.startswith("_") and key not in exclude:
                value = getattr(self, key)
                if isinstance(value, datetime):
                    value = str(value)
                data[key] = value
        return data