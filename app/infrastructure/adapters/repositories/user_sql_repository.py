from typing import List, Optional
from app.domain.entities.user import UserModel
from app.application.ports.user_repository_port import UserRepositoryPort
from app.infrastructure.mappers.user_mapper import UserMapper
from app.application.ports.db_client_port import DbClientPort
from datetime import date
from app.domain.enums.role import RoleEnum

class UserSqlRepository(UserRepositoryPort):
    def __init__(self, session: DbClientPort):
        self.session = session

    def get_all(self) -> List[UserModel]:
        rows = self.session.fetch_all("SELECT id, firstName, lastName, email, password, dateOfBirth, roleId FROM users")
        return [UserMapper.to_model(row) for row in rows]

    def create(self, firstName: str, lastName: str, email: str, password: str, dateOfBirth: date):
        role_id = RoleEnum.USER.value
        self.session.execute(
            "INSERT INTO users (firstName, lastName, email, password, dateOfBirth, roleId) VALUES (?, ?, ?, ?, ?, ?)",
            (firstName, lastName, email, password, dateOfBirth.strftime("%Y-%m-%d"), role_id),
        )

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        row = self.session.fetch_one(
            "SELECT id, firstName, lastName, email, password, dateOfBirth, roleId FROM users WHERE id = ?",
            (user_id,),
        )
        if row:
            return UserMapper.to_model(row)
        return None

    def get_by_email(self, email: str) -> Optional[UserModel]:
        row = self.session.fetch_one(
            "SELECT id, firstName, lastName, email, password, dateOfBirth, roleId FROM users WHERE email = ?",
            (email,),
        )
        if row:
            return UserMapper.to_model(row)
        return None
    
    def update(self, user_id: int, firstName: str, lastName: str, email: str, dateOfBirth: date):
        self.session.execute(
            "UPDATE users SET firstName = ?, lastName = ?, email = ?, dateOfBirth = ? WHERE id = ?",
            (firstName, lastName, email, dateOfBirth.strftime("%Y-%m-%d"), user_id),
        )

    def delete(self, user_id: int):
        self.session.execute("DELETE FROM users WHERE id = ?", (user_id,))
