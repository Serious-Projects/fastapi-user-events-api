from fastapi import APIRouter, Depends, status

from app.api.schema.user import UpdateUser, UserOut
from app.api.services import UserService, get_user_service
from app.utils.jwt import CurrentLoggedInUser

userRouter = APIRouter(prefix="/users")


@userRouter.get("", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_users(user_service: UserService = Depends(get_user_service)):
    users = user_service.get_all()
    return users


@userRouter.get("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_me(curr_user: CurrentLoggedInUser):
    return curr_user


@userRouter.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = user_service.get(user_id)
    return user


@userRouter.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def update_user(
    user_id: int,
    user_patch: UpdateUser,
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.update(user_id, user_patch)
    return user


@userRouter.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user_service.delete(user_id)
    return
