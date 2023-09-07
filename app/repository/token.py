from sqlalchemy.orm import Session
import app.models as models
from fastapi import HTTPException, status
from app.config import settings
import requests

def get_token(username: str, password: str, db: Session):
    url = settings.API_BASE_URL + settings.GET_TOKEN_ENDPOINT

    payload=f'grant_type=password&username={username}&password={password}'
    headers = {
        'CLIENT_ID': settings.AUTH_CLIENT_ID,
        'CLIENT_SECRET': settings.AUTH_CLIENT_SECRET,
        'Authorization': settings.AUTH_AUTHORIZATION,
        'Content-Type': settings.AUTH_CONTENT_TYPE
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        return response.json()
    else:
        return {"message": "Error authenticating User!"}