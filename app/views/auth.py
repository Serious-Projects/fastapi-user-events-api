from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..database.connection import Session
from ..models.user import User
from ..schema.auth import TokenBody
from ..security import ACCESS_TOKEN_EXPIRATION_TIME, create_access_token
from ..utils.hashing import verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenBody)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session
) -> TokenBody:
    user = session.query(User).filter_by(name=form_data.username).first()
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

    access_token_expires_in = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME)
    access_token = create_access_token(
        data={"sub": user.name}, expires_in=access_token_expires_in
    )

    return TokenBody(access_token=access_token, type="bearer")
