from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.api.models.user import UserModel
from app.api.schema.auth import CurrentUser
from app.config import Settings, get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

Token = Annotated[str, Depends(oauth2_scheme)]


def create_access_token(
    data: dict,
    config: Settings,
    expires_in: Optional[timedelta] = None,
):
    to_encode = data.copy()
    if expires_in:
        expire = datetime.utcnow() + expires_in
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt_token = jwt.encode(
        to_encode, config.HASH_SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt_token


def authenticate_user(token: Token) -> UserModel:
    from app.api.services import UserService, get_user_service

    user_service: UserService = get_user_service()
    config: Settings = get_settings()
    hash_secret_key = config.HASH_SECRET_KEY
    algorithm = config.ALGORITHM

    try:
        payload = jwt.decode(token, hash_secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = user_service.get_by_filter(name=username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


CurrentLoggedInUser = Annotated[CurrentUser, Depends(authenticate_user)]
