from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.role import RoleModel

class RoleRepositoryPort(ABC):
    @abstractmethod
    def get_all(self) -> List[RoleModel]:
        pass

    @abstractmethod
    def get_by_id(self, role_id: int) -> Optional[RoleModel]:
        pass
