from typing import List, Optional
from app.repository.models.role_model import RoleModel
from app.db.dependencies import LocalDb

class RoleRepository:
    def __init__(self, session: LocalDb):
        self.session = session

    def get_all(self) -> List[RoleModel]:
        rows = self.session.fetch_all("SELECT id, name, description FROM roles")
        return [RoleModel(id=row[0], name=row[1], description=row[2]) for row in rows]

    def create(self, name: str, description: str):
        self.session.execute(
            "INSERT INTO roles (name, description) VALUES (?, ?)",
            (name, description),
        )

    def get_by_id(self, role_id: int) -> Optional[RoleModel]:
        row = self.session.fetch_one(
            "SELECT id, name, description FROM roles WHERE id = ?",
            (role_id,),
        )
        if row:
            return RoleModel(id=row[0], name=row[1], description=row[2])
        return None
