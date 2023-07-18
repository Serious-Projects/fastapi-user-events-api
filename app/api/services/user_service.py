from typing import Any, Union

from ..repositories.user_repository import UserRepository
from ..schema.user import UpdateUser, UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository

    def get(self, id: Union[int, str]):
        return self._repository.get_by_id(id)

    def get_all(self):
        return self._repository.get_all()

    def get_by_filter(self, **filter: Any):
        return self._repository.get_by_filter(**filter)

    def get_all_by_filter(self, **filter):
        return self._repository.get_all_by_filter(**filter)

    def create(self, user: UserCreate):
        return self._repository.create(user)

    def update(self, id: Union[int, str], user: UpdateUser):
        return self._repository.update(id, user)

    def delete(self, id: Union[int, str]):
        return self._repository.delete(id)

    def exists(self, id: Union[int, str]) -> bool:
        user = self.get(id)
        return user is not None
