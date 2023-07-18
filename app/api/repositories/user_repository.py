from typing import Any, Optional, Union

from sqlalchemy.orm import Session

from ..models.user import UserModel
from ..schema.user import UpdateUser, UserCreate
from ...database.connection import get_db
from ...utils.hashing import hash_password


class UserRepository:
    _db: Session

    def __init__(self, db: Optional[Session] = None):
        # using `next(get_db())` because it is a generator function that automatically
        # creates a context manager for each session to properly handle the resources
        self._db = db if db is not None else next(get_db())

    def get_by_id(self, id: Union[int, str]) -> Optional[UserModel]:
        return self._db.query(UserModel).get(id)

    def get_all(self) -> list[UserModel]:
        return self._db.query(UserModel).all()

    def get_by_filter(self, **filter: Any) -> UserModel:
        return self._db.query(UserModel).filter_by(**filter).first()

    def get_all_by_filter(self, **filter) -> list[UserModel]:
        return self._db.query(UserModel).filter_by(**filter).all()

    def create(self, user: UserCreate) -> UserModel:
        hashed_password = hash_password(user.password)
        user_create = UserModel(name=user.name, email=user.email, password=hashed_password)  # fmt: skip
        self._db.add(user_create)
        self._db.commit()
        self._db.refresh(user_create)
        return user_create

    def exists(self, id: Union[int, str]) -> bool:
        user = self.get_by_id(id)
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
