from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user import UserModel
from datetime import date

class UserRepositoryPort(ABC):
    @abstractmethod
    def get_all(self) -> List[UserModel]:
        pass

    @abstractmethod
    def create(self, firstName: str, lastName: str, email: str, password: str, dateOfBirth: date):
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserModel]:
        pass

    @abstractmethod
    def update(self, user_id: int, firstName: str, lastName: str, email: str, dateOfBirth: date):
        pass

    @abstractmethod
    def delete(self, user_id: int):
        pass
