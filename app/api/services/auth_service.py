from datetime import timedelta
from typing import TYPE_CHECKING

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..schema.auth import TokenBody, UserCredentials
from ...config import Settings, get_settings
from ...utils.hashing import verify_password
from ...utils.jwt import create_access_token

if TYPE_CHECKING:
    from app.api.services import UserService


class AuthenticationService:
    def __init__(self, user_service: "UserService"):
        self._user_service = user_service

    def login(self, form_data: OAuth2PasswordRequestForm) -> TokenBody:
        config: Settings = get_settings()

        user = self._user_service.get_by_filter(name=form_data.username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Seems like you haven't registered yet.",
            )

        if not verify_password(form_data.password, str(user.password)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires_in = timedelta(minutes=config.ACCESS_TOKEN_EXPIRATION_TIME)
        access_token = create_access_token(
            data={"sub": user.name},
            expires_in=access_token_expires_in,
            config=config,
        )

        return TokenBody(access_token=access_token, type="bearer")

    def login_new(self, form_data: UserCredentials) -> TokenBody:
        config: Settings = get_settings()

        user = self._user_service.get_by_filter(name=form_data.username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Seems like you haven't registered yet.",
            )

        if not verify_password(form_data.password, str(user.password)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires_in = timedelta(minutes=config.ACCESS_TOKEN_EXPIRATION_TIME)
        access_token = create_access_token(
            data={"sub": user.name},
            expires_in=access_token_expires_in,
            config=config,
        )

        return TokenBody(access_token=access_token, type="bearer")
