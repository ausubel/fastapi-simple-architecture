from typing import List
from app.repository.models.user_model import UserModel
from app.repository.user_repository import UserRepository
from datetime import date

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all(self) -> List[UserModel]:
        return self.user_repository.get_all()
    
    def create(self, firstName: str, lastName: str, email: str, dateOfBirth: date):
        self.user_repository.create(firstName, lastName, email, dateOfBirth)

    def get_by_id(self, user_id: int) -> UserModel:
        return self.user_repository.get_by_id(user_id)
    
    def update(self, user_id: int, firstName: str, lastName: str, email: str, dateOfBirth: date):
        self.user_repository.update(user_id, firstName, lastName, email, dateOfBirth)

    def delete(self, user_id: int):
        self.user_repository.delete(user_id)