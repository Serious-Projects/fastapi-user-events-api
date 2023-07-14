from fastapi import APIRouter, status

from ...database.connection import Session
from ...security.auth_tokens import CurrentLoggedInUser
from ..schema.user import UpdateUser, UserOut

userRouter = APIRouter()


def get_users(db: Session):
    # users = userService.get_all_users(db)
    # return users
    pass


@userRouter.get("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_me(curr_user: CurrentLoggedInUser):
    return curr_user


@userRouter.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(user_id: int, db: Session):
    # user = userService.get_user_by(user_id, db)
    return


@userRouter.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def update_user(user_id: int, user_patch: UpdateUser, db: Session):
    # user = userService.update_user(db, user_id, user_patch)
    return


@userRouter.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session):
    return
