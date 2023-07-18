from typing import List

from fastapi import APIRouter, Depends, status

from ..models.user import UserModel
from ..schema.user import UpdateUser, UserOut
from ..services import UserService, get_user_service
from ...utils.jwt import CurrentLoggedInUser

user_router = APIRouter(prefix="/users", tags=["User Routes"])


@user_router.get("", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_users(user_service: UserService = Depends(get_user_service)) -> List[UserModel]:
    return user_service.get_all()


@user_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_me(curr_user: CurrentLoggedInUser) -> CurrentLoggedInUser:
    return curr_user


@user_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
) -> UserModel:
    return user_service.get(user_id)


@user_router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def update_user(
    user_id: int,
    user_patch: UpdateUser,
    user_service: UserService = Depends(get_user_service),
) -> UserModel:
    return user_service.update(user_id, user_patch)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
) -> None:
    user_service.delete(user_id)
