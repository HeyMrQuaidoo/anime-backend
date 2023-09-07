from typing import Dict
from datetime import datetime
import json
from typing import Any, Optional
from pydantic import BaseModel
from sqlalchemy import JSON

class User(BaseModel):
    id: Optional[str]
    username: Optional[str]
    email: Optional[str]
    avatar: Optional[str]
    favorites: Optional[Any]

    class Config():
        orm_mode = True

class UserCreateRequest(User):
    username: Optional[str]
    email: Optional[str]
    avatar: Optional[str]
    id:Optional[str]

    class Config():
        orm_mode = True

class UserResponse(User):
    id: Optional[str]
    username: Optional[str]
    email: Optional[str]
    avatar: Optional[str]
    access_token: Optional[str]
    refresh_token: Optional[str]
    last_login_time: Optional[datetime]

    class Config():
        orm_mode = True

class UserUpdateRequest(User):
    id: Optional[str]
    username: Optional[str]
    email: Optional[str]
    avatar: Optional[str]
    favorites: Optional[Any]

    class Config():
        orm_mode = True