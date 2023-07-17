from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from app.api.schema.auth import TokenBody, UserCredentials
from app.api.schema.user import UserCreate, UserOut
from app.api.services import get_auth_service, get_user_service
from app.api.services.auth_service import AuthenticationService
from app.api.services.user_service import UserService

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenBody)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> TokenBody:
    return auth_service.login(form_data)


@auth_router.post(
    "/login-new", status_code=status.HTTP_200_OK, response_model=TokenBody
)
def login_new(
    form_data: UserCredentials,
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> TokenBody:
    return auth_service.login_new(form_data)


@auth_router.post("/register", status_code=status.HTTP_200_OK, response_model=UserOut)
def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.create(user)
