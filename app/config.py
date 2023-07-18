from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "User Event API"
    SQLITE_DB_URL_ASYNC: str = ""
    SQLITE_DB_URL: str = ""
    JWT_SECRET_KEY: str = ""
    HASH_SECRET_KEY: bytes = b""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRATION_TIME: int = 15

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
