from pathlib import Path
import os
from fastapi import Depends
from typing import Annotated
from app.db.clients.db_client import DbClient
from app.db.clients.sqlite_client import SqliteClient
from app.db.clients.postgres_client import PostgresClient

def get_db_client():
        dsn = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/fastapi_db")
        yield PostgresClient.get_instance(dsn)
        # db_path = Path(path_str) if path_str else Path(__file__).resolve().parent.parent.parent / "database.db"
        # yield SqliteClient.get_instance(db_path)

LocalDb = Annotated[DbClient, Depends(get_db_client)]
