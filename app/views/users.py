from fastapi import APIRouter, status

from ..database.connection import Session
from ..models.user import UserModel
from ..schema.user import UpdateUser, UserCreate, UserOut
from ..security import CurrentLoggedInUser
from ..services import user as userService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", status_code=status.HTTP_200_OK, response_model=list[UserOut])
def get_users(db: Session):
    users = db.query(UserModel).all()
    return users


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_me(curr_user: CurrentLoggedInUser):
    return curr_user


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(user_id: int, db: Session):
    user = userService.get_user_by(user_id, db)
    return user


@router.post("", status_code=status.HTTP_200_OK, response_model=UserOut)
def create_user(user: UserCreate, db: Session):
    user = userService.create_user(db, user)
    return user


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def update_user(user_id: int, user_patch: UpdateUser, db: Session):
    user = userService.update_user(db, user_id, user_patch)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session):
    userService.delete_user(db, user_id)
