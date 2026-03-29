from typing import List, Optional
from app.domain.entities.user import UserModel
from app.application.ports.user_repository_port import UserRepositoryPort
from datetime import date

class UserService:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def get_all(self) -> List[UserModel]:
        return self.user_repository.get_all()
    
    def create(self, firstName: str, lastName: str, email: str, password: str, dateOfBirth: date):
        self.user_repository.create(firstName, lastName, email, password, dateOfBirth)

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return self.user_repository.get_by_id(user_id)

    def get_by_email(self, email: str) -> Optional[UserModel]:
        return self.user_repository.get_by_email(email)
    
    def update(self, user_id: int, firstName: str, lastName: str, email: str, dateOfBirth: date):
        self.user_repository.update(user_id, firstName, lastName, email, dateOfBirth)

    def delete(self, user_id: int):
        self.user_repository.delete(user_id)
