import json

from pydantic import Json
import app.utils.constants as c
from sqlalchemy.orm import Session
import app.models as models, app.schema.user as schemas
from fastapi import HTTPException, status
import uuid
from app.config import settings
import requests

def authenticate_user(authorization, access_token, refresh_token, username, db: Session):
    url = settings.API_BASE_URL + settings.USERS_ENDPOINT + "?filter[name]=" + username
    headers = {'Authorization': authorization, 'Content-Type': 'application/vnd.api+json'}
    response = requests.request("GET", url, headers=headers, data={})

    if response.ok:
        data = response.json()
        item = data['data'][0]

        # check if user exists
        user = db.query(models.User).filter_by(id=item['id']).first()

        if not user:
            create_user = models.User(
                id=item['id'],
                avatar=item['attributes']['avatar']['medium'],
                username=item['attributes']['name'],
                access_token=access_token,
                refresh_token=refresh_token
            )
            db.add(create_user)
            db.commit()
        else:
            # Update the access_token and refresh_token
            user.access_token = access_token
            user.refresh_token = refresh_token

            db.commit()
            db.refresh(user)

            print(f"{c.USER_AUTH_TOKEN_UPDATE_SUCCESS} {user.id}")
    else:
        return {"message": c.ERROR_AUTHENTICATING_USER}

    return response.json()

def add_favorite(id: str, request: schemas.UserUpdateRequest, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{c.USER_WITH_ID_NOT_FOUND} {id}")
    user.favorites = json.loads(request.favorites)

    db.commit()
    db.refresh(user)

    return user

async def create(request: schemas.User, db: Session) -> models.User:

    # check if the user with the given id already exists
    user = db.query(models.User).filter_by(id=request.id).first()
    print(user, request.id)
    if user:
        error_message = f"User with this id: {request.id} already exists."
        raise HTTPException(status_code=400, detail=error_message)
    
    new_user = models.User(
        id=request.id,
        avatar=request.avatar,
        username=request.username,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user

def get_all(db: Session):
    users = db.query(models.User).all()
    
    if len(users) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{c.USER_NOT_FOUND}")
    return users

def show(id: str, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{c.USER_WITH_ID_NOT_FOUND} {id}")
    
    return user

def update(id: str, request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{c.USER_WITH_ID_NOT_FOUND} {id}")

    for field in request.dict(exclude_unset=True):
        setattr(user, field, request.dict()[field])

    db.commit()

    db.refresh(user)
    return user

def destroy(id: str, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    
    if not user.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"{c.USER_WITH_ID_NOT_FOUND} {id}")
    
    user_del = user.first()
    user_id = user_del.id

    user.delete(synchronize_session=False)
    db.commit()

    return user