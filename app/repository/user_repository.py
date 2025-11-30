from typing import List
from app.repository.models.user_model import UserModel
from app.repository.mappers.user_mapper import UserMapper
from app.db.database_session import LocalSession
from datetime import date

class UserRepository:
    def __init__(self, session: LocalSession):
        self.session = session

    def get_all(self) -> List[UserModel]:
        cursor = self.session.cursor()
        cursor.execute("SELECT id, firstName, lastName, email, dateOfBirth FROM users")
        rows = cursor.fetchall()
        return [UserMapper.to_model(row) for row in rows]

    def create(self, firstName: str, lastName: str, email: str, dateOfBirth: date):
        cursor = self.session.cursor()
        cursor.execute("INSERT INTO users (firstName, lastName, email, dateOfBirth) VALUES (?, ?, ?, ?)",
                       (firstName, lastName, email, dateOfBirth.strftime("%Y-%m-%d")))
        self.session.commit()

    def get_by_id(self, user_id: int) -> UserModel:
        cursor = self.session.cursor()
        cursor.execute("SELECT id, firstName, lastName, email, dateOfBirth FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return UserMapper.to_model(row)
        return None
    
    def update(self, user_id: int, firstName: str, lastName: str, email: str, dateOfBirth: date):
        cursor = self.session.cursor()
        cursor.execute("UPDATE users SET firstName = ?, lastName = ?, email = ?, dateOfBirth = ? WHERE id = ?",
                       (firstName, lastName, email, dateOfBirth.strftime("%Y-%m-%d"), user_id))
        self.session.commit()

    def delete(self, user_id: int):
        cursor = self.session.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.session.commit()