from fastapi import APIRouter, HTTPException, status

from ..database.connection import Session
from ..models.user import UserModel
from ..schema.user import UpdateUser, UserIn, UserOut
from ..security import CurrentLoggedInUser
from ..security.hashing import hash_password

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
    user = db.query(UserModel).get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist!"
        )
    print(user.events)
    return user


@router.post("", status_code=status.HTTP_200_OK, response_model=UserOut)
def create_user(user: UserIn, db: Session):
    # User object
    hashed_password = hash_password(user.password)
    user = UserModel(name=user.name, email=user.email, password=hashed_password)
    # Save the user to the database
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def update_user(user_id: int, user_patch: UpdateUser, db: Session):
    user = db.query(UserModel).get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User was not found!"
        )

    # Update the user
    update_data = user_patch.dict(exclude_unset=True)
    for key, value in update_data.items():
        # update the field with user provided data
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session):
    user = db.query(UserModel).get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User was not found!"
        )

    # Delete the user from the database
    db.delete(user)
    db.commit()
