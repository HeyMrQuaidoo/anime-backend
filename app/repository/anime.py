import json
import app.utils.constants as c
from sqlalchemy.orm import Session
import app.models as models, app.schema.user as schemas
from fastapi import HTTPException, status
import uuid
from app.config import settings
import requests

def get_anime(authorization,  db: Session):
    url = settings.API_BASE_URL + settings.ANIME_ENDPOINT
    headers = {'Authorization': authorization, 'Content-Type': 'application/vnd.api+json'}
    response = requests.request("GET", url, headers=headers, data={})

    if response.ok:
        data = response.json()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{c.ERROR_FETCHING_ANIME}")
    return data