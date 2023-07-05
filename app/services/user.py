from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import UserModel
from ..schema.user import UpdateUser, UserIn
from ..security.hashing import hash_password


def get_user_by(id: int, db: Session) -> UserModel:
    user = db.query(UserModel).get(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    return user


def create_user(db: Session, user: UserIn) -> UserModel:
    hashed_password = hash_password(user.password)
    new_user = UserModel(**user, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def check_user_exists(db: Session, id: int) -> bool:
    user = db.query(UserModel).get(id)
    return user is not None


def update_user(db: Session, id: int, patch_data: UpdateUser) -> UserModel:
    user = get_user_by(id, db)
    # Update the user
    user_dict = patch_data.dict(exclude_unset=True)
    for key, value in user_dict.items():
        # update the user object's field with user provided data
        setattr(user, key, value)
    # push the changes to the database
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, id: int) -> UserModel:
    user = get_user_by(id, db)
    db.delete(user)
    db.commit()
    return user
