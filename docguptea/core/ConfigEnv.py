"""Config class for handling env variables.
"""
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER: str
    DATABASE: str
    UID: str
    PASSWORD: str
    DRIVER: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


config = get_settings()
