"""Config class for handling env variables.
"""
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    HOSTNAME: str
    DATABASE: str
    USER: str
    PASSWORD: str
    ALGORITHM:str
    JWT_SECRET_KEY:str
    JWT_REFRESH_SECRET_KEY:str
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


config = get_settings()
