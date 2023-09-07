import json
from fastapi import APIRouter
from typing import List

from fastapi.responses import JSONResponse
from pydantic import Json
import app.db.database as database, app.schema.user as schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from app.repository import user as user_service

router = APIRouter(
    prefix="/api/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=schemas.UserResponse)
async def create_user(request: schemas.UserCreateRequest, db: Session = Depends(get_db)):
    return await user_service.create(request, db)

@router.get('/', response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_all(db)

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: str, db: Session = Depends(get_db)):
    return user_service.show(id, db)

@router.put('/favorites/{id}', response_model=schemas.UserResponse)
def add_favorites(id: str, request: schemas.UserUpdateRequest, db: Session = Depends(get_db)):
    user_with_favorites = user_service.add_favorite(id, request, db)
    
    return user_with_favorites

@router.put('/{id}',response_model=schemas.UserResponse) 
def update_user(id: str, request: schemas.UserUpdateRequest, db: Session = Depends(get_db)):
    return user_service.update(id, request, db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT ) 
def destroy_user(id: str, db: Session = Depends(get_db)):
    return user_service.destroy(id, db)