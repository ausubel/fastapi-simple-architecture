from typing import Optional, Sequence, Any
from .db_client import DbClient

class PostgresClient:
    _instance: Optional["PostgresClient"] = None
    def __init__(self, dsn: str):
        import psycopg2
        self.conn = psycopg2.connect(dsn)
    @classmethod
    def get_instance(cls, dsn: str) -> DbClient:
        if cls._instance is None:
            cls._instance = PostgresClient(dsn)
        return cls._instance
    def _adapt(self, query: str) -> str:
        return query.replace("?", "%s")
    def fetch_all(self, query: str, params: Optional[Sequence[Any]] = None) -> list[tuple]:
        cur = self.conn.cursor()
        cur.execute(self._adapt(query), params or [])
        rows = cur.fetchall()
        cur.close()
        return rows
    def fetch_one(self, query: str, params: Optional[Sequence[Any]] = None) -> Optional[tuple]:
        cur = self.conn.cursor()
        cur.execute(self._adapt(query), params or [])
        row = cur.fetchone()
        cur.close()
        return row
    def execute(self, query: str, params: Optional[Sequence[Any]] = None) -> int:
        cur = self.conn.cursor()
        cur.execute(self._adapt(query), params or [])
        self.conn.commit()
        try:
            res = cur.fetchone()
            cur.close()
            return res[0] if res else 0
        except Exception:
            cur.close()
            return 0
