from pathlib import Path
import sqlite3
from typing import Optional, Sequence, Any
from .db_client import DbClient

class SqliteClient:
    _instance: Optional["SqliteClient"] = None
    def __init__(self, db_path: Path):
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
    @classmethod
    def get_instance(cls, db_path: Path) -> DbClient:
        if cls._instance is None:
            cls._instance = SqliteClient(db_path)
        return cls._instance
    def fetch_all(self, query: str, params: Optional[Sequence[Any]] = None) -> list[tuple]:
        cur = self.conn.cursor()
        cur.execute(query, params or [])
        return cur.fetchall()
    def fetch_one(self, query: str, params: Optional[Sequence[Any]] = None) -> Optional[tuple]:
        cur = self.conn.cursor()
        cur.execute(query, params or [])
        return cur.fetchone()
    def execute(self, query: str, params: Optional[Sequence[Any]] = None) -> int:
        cur = self.conn.cursor()
        cur.execute(query, params or [])
        self.conn.commit()
        try:
            return cur.lastrowid
        except Exception:
            return 0
