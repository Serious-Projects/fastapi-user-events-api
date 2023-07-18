from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from ..schema.auth import TokenBody, UserCredentials
from ..schema.user import UserCreate, UserOut
from ..services import get_auth_service, get_user_service
from ..services.auth_service import AuthenticationService
from ..services.user_service import UserService

auth_router = APIRouter(prefix="/auth", tags=["Authentication Routes"])


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
