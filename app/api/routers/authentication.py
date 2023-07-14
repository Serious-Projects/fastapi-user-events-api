from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from ...config import AppSettings
from ...database.connection import Session
from ...security.auth_tokens import create_access_token
from ...security.hashing import verify_password
from ..models.user import UserModel
from ..schema.auth import TokenBody, UserCredentials
from ..schema.user import UserCreate, UserOut

authRouter = APIRouter()


@authRouter.post("/login", status_code=status.HTTP_200_OK, response_model=TokenBody)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session,
    config: AppSettings,
) -> TokenBody:
    user = session.query(UserModel).filter_by(name=form_data.username).first()
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
        data={"sub": user.name}, expires_in=access_token_expires_in, config=config
    )

    return TokenBody(access_token=access_token, type="bearer")


@authRouter.post("/login-new", status_code=status.HTTP_200_OK, response_model=TokenBody)
def login_new(
    form_data: UserCredentials, session: Session, config: AppSettings
) -> TokenBody:
    user = session.query(UserModel).filter_by(name=form_data.username).first()
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
        data={"sub": user.name}, expires_in=access_token_expires_in, config=config
    )

    return TokenBody(access_token=access_token, type="bearer")


@authRouter.post("/register", status_code=status.HTTP_200_OK, response_model=UserOut)
def create_user(user: UserCreate, db: Session):
    # user = user_service.create_user(db, user)
    return
