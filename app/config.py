from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "User Event API"
    sqlite_db_url_async: str = ""
    sqlite_db_url: str = ""
    jwt_secret_key: str = ""
    hash_secret_key: bytes = b""
    algorithm: str = ""
    access_token_expiration_time: int = 15

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


AppSettings = Annotated[Settings, Depends(get_settings)]

config = Settings()
