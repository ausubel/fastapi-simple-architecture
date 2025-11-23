from pathlib import Path
from fastapi import Depends
import sqlite3
from typing import Annotated

database_dir = Path(__file__).resolve().parent.parent.parent / "database.db"
print(database_dir)
conn = sqlite3.connect(str(database_dir), check_same_thread=False)

cursor = conn.cursor()

def get_session():
    with conn as session:
        yield session

LocalSession = Annotated[sqlite3.Connection, Depends(get_session)]
