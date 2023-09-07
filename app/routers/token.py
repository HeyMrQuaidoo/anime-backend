from typing import List, Annotated, Union
import app.db.database as database, app.schema.user as schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Form, Header
from app.repository import token as token_service
from app.repository import user as user_service

router = APIRouter(
    prefix="/api",
    tags=['Token']
)

get_db = database.get_db

@router.post('/oauth/token')
def get_token(grant_type: Annotated[str, Form()], username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    return token_service.get_token(username, password, db)

@router.get('/edge/users/{username}')
def get_token(username: str, Authorization: Annotated[Union[str, None], Header()] = None, accessToken: Annotated[Union[str, None], Header()] = None, refreshToken: Annotated[Union[str, None], Header()] = None, db: Session = Depends(get_db)):
    return user_service.authenticate_user(Authorization, accessToken, refreshToken, username, db)