from sqlalchemy.orm import Session

from ..api.models import UserModel
from ..api.schema.user import UpdateUser, UserCreate
from ..security.hashing import hash_password
from ..utils.exceptions import EmptyTableException, EntityNotFoundException


def get_user_by(id: int, db: Session) -> UserModel:
    user = db.query(UserModel).get(id)
    if user is None:
        raise EntityNotFoundException("user not found")
    return user


def get_all_users(db: Session) -> list[UserModel]:
    users = db.query(UserModel).all()
    if len(users) == 0:
        raise EmptyTableException()
    return users


def get_user_by_filter(db: Session, **kwargs) -> UserModel:
    user = db.query(UserModel).filter_by(**kwargs).first()
    return user


def get_users_by_filter(db: Session, **kwargs) -> list[UserModel]:
    users = db.query(UserModel).filter_by(**kwargs).all()
    return users


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    new_user = UserModel(name=user.name, email=user.email, password=hashed_password)
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
