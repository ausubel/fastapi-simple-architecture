from abc import ABC, abstractmethod
from typing import Optional, Sequence, Any

class DbClientPort(ABC):
    @abstractmethod
    def fetch_all(self, query: str, params: Optional[Sequence[Any]] = None) -> list[tuple]:
        pass

    @abstractmethod
    def fetch_one(self, query: str, params: Optional[Sequence[Any]] = None) -> Optional[tuple]:
        pass

    @abstractmethod
    def execute(self, query: str, params: Optional[Sequence[Any]] = None) -> int:
        pass
