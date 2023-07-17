from typing import Any, Union

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.models.user import UserModel
from app.api.schema.user import UpdateUser, UserCreate
from app.database.connection import get_db
from app.utils.exceptions import EntityNotFoundException
from app.utils.hashing import hash_password


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self._db = db

    def get_by_id(self, id: Union[int, str]) -> UserModel:
        user = self._db.query(UserModel).get(id)
        if user is None:
            raise EntityNotFoundException("user not found")
        return user

    def get_all(self) -> list[UserModel]:
        users = self._db.query(UserModel).all()
        return users

    def get_by_filter(self, **filter: Any) -> UserModel:
        user = self._db.query(UserModel).filter_by(**filter).first()
        return user

    def get_all_by_filter(self, **filter) -> list[UserModel]:
        users = self._db.query(UserModel).filter_by(**filter).all()
        return users

    def create(self, user: UserCreate) -> UserModel:
        hashed_password = hash_password(user.password)
        user_create = UserModel(
            name=user.name, email=user.email, password=hashed_password
        )
        self._db.add(user_create)
        self._db.commit()
        self._db.refresh(user_create)
        return user_create

    def exists(self, id: Union[int, str]) -> bool:
        user = self._db.query(UserModel).get(id)
        return user is not None

    def update(self, id: Union[int, str], patch_data: UpdateUser) -> UserModel:
        user = self.get_by_id(id)
        # Update the user
        user_dict = patch_data.dict(exclude_unset=True)
        for key, value in user_dict.items():
            # update the user object's field with user provided data
            setattr(user, key, value)
        # push the changes to the database
        self._db.commit()
        self._db.refresh(user)
        return user

    def delete(self, id: Union[int, str]) -> UserModel:
        user = self.get_by_id(id)
        self._db.delete(user)
        self._db.commit()
        return user
