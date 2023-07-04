from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing_extensions import Annotated

from ..config import AppSettings, Settings, get_settings
from ..database.connection import Session
from ..models.user import UserModel

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
        to_encode, config.hash_secret_key, algorithm=config.algorithm
    )
    return encoded_jwt_token


def authenticate_user_from(token: Token, db: Session, config: AppSettings):
    try:
        payload = jwt.decode(
            token, config.hash_secret_key, algorithms=[config.algorithm]
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(UserModel).filter_by(name=username).first()
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


CurrentLoggedInUser = Annotated[UserModel, Depends(authenticate_user_from)]
