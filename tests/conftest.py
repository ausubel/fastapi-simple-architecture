import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.db.dependencies import get_db_client
from app.db.clients.sqlite_client import SqliteClient
from main import app

# Create a clean SQLite in-memory database for testing
# This assumes the app uses raw SQL compatible with SQLite or the client handles it.
INIT_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    dateOfBirth TEXT NOT NULL,
    roleId INTEGER NOT NULL
);
"""

@pytest.fixture
def test_db_client():
    # Use in-memory SQLite for tests
    # We pass ":memory:" string which sqlite3 accepts
    client = SqliteClient(":memory:")
    
    # Initialize the database schema
    client.execute(INIT_SQL)
    
    return client

@pytest.fixture
def client(test_db_client):
    # Override the get_db_client dependency to return our test client
    app.dependency_overrides[get_db_client] = lambda: test_db_client
    return TestClient(app)
