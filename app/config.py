from pydantic import BaseSettings
import os

current_dir = os.path.dirname(__file__)

class Settings(BaseSettings):

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret: str
    algorithm: str
    access_token_expire_minutes: int
    AUTH_CLIENT_ID: str
    AUTH_CLIENT_SECRET: str
    AUTH_CONTENT_TYPE: str
    AUTH_AUTHORIZATION: str
    API_BASE_URL: str
    GET_TOKEN_ENDPOINT: str
    REFRESH_TOKEN_ENDPOINT: str
    JOKE_ENDPOINT: str
    JOKE_RANDOM_ENDPOINT: str
    ANIME_ENDPOINT: str
    USERS_ENDPOINT: str
    LOGOUT_ENDPOINT: str

    class Config:
        env_file = ".env"

settings = Settings()