from typing import Annotated, Union
import app.db.database as database
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header
from app.repository import anime as anime_service

router = APIRouter(
    prefix="/api",
    tags=['Anime']
)

get_db = database.get_db

@router.get('/edge/anime/')
def get_anime(Authorization: Annotated[Union[str, None], Header()] = None, db: Session = Depends(get_db)):
    return anime_service.get_anime(Authorization, db)