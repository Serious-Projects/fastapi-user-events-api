from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.models.user import UserModel
from app.api.schema.user import UpdateUser, UserCreate
from app.security.hashing import hash_password
from app.utils.exceptions import EmptyTableException, EntityNotFoundException

from ...database.connection import get_db


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db_session = db

    def get_user(self, id: int | str) -> UserModel:
        user = self.db_session.query(UserModel).get(id)
        if user is None:
            raise EntityNotFoundException("user not found")
        return user

    def get_all_users(self) -> list[UserModel]:
        users = self.db_session.query(UserModel).all()
        return users

    def get_user_by_filter(self, **kwargs) -> UserModel:
        user = self.db_session.query(UserModel).filter_by(**kwargs).first()
        return user

    def get_users_by_filter(self, **kwargs) -> list[UserModel]:
        users = self.db_session.query(UserModel).filter_by(**kwargs).all()
        return users

    def create_user(self, user: UserCreate):
        hashed_password = hash_password(user.password)
        new_user = UserModel(name=user.name, email=user.email, password=hashed_password)
        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)
        return new_user

    def check_user_exists(self, id: int) -> bool:
        user = self.db_session.query(UserModel).get(id)
        return user is not None

    def update_user(self, id: int, patch_data: UpdateUser) -> UserModel:
        user = self.get_user(id)
        # Update the user
        user_dict = patch_data.dict(exclude_unset=True)
        for key, value in user_dict.items():
            # update the user object's field with user provided data
            setattr(user, key, value)
        # push the changes to the database
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def delete_user(self, id: int) -> UserModel:
        user = self.get_user(id)
        self.db_session.delete(user)
        self.db_session.commit()
        return user
