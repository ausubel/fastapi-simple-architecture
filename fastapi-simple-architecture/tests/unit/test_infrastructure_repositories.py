"""
Tests for Infrastructure Layer - SQL Repositories

La capa de infraestructura conecta con la base de datos.
Usamos SQLite en memoria para testear sin afectar datos reales.
"""

import sqlite3
import pytest
from datetime import datetime

from app.infrastructure.adapters.repositories.post_sql_repository import PostSqlRepository
from app.infrastructure.adapters.repositories.user_sql_repository import UserSqlRepository
from app.infrastructure.adapters.db.clients.sqlite_client import SqliteClient


class TestSqliteClient:
    """Cliente SQLite simple para pruebas."""
    
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
    
    def fetch_all(self, query, params=None):
        cursor = self.conn.execute(query, params or ())
        return cursor.fetchall()
    
    def fetch_one(self, query, params=None):
        cursor = self.conn.execute(query, params or ())
        return cursor.fetchone()
    
    def execute(self, query, params=None):
        self.conn.execute(query, params or ())
        self.conn.commit()


@pytest.fixture
def db_client():
    """Fixture que crea una base de datos SQLite en memoria con tablas."""
    client = TestSqliteClient()
    
    # Creamos las tablas necesarias
    client.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT,
            lastName TEXT,
            email TEXT,
            password TEXT,
            dateOfBirth TEXT,
            roleId INTEGER
        )
    """)
    
    client.execute("""
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            userId INTEGER,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insertamos un usuario de prueba
    client.execute(
        "INSERT INTO users (id, firstName, lastName, email, password, dateOfBirth, roleId) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (1, "John", "Doe", "john@example.com", "pass", "1990-01-01", 1)
    )
    
    yield client
    client.conn.close()


def test_post_repository_create_and_get(db_client):
    """Test: Crear un post y luego recuperarlo."""
    repo = PostSqlRepository(db_client)
    
    # Creamos un post
    repo.create("Test Title", "Test Content", 1)
    
    # Verificamos que se creó
    posts = repo.get_all()
    assert len(posts) == 1
    assert posts[0].title == "Test Title"
    assert posts[0].content == "Test Content"
    assert posts[0].userId == 1


def test_post_repository_get_by_id(db_client):
    """Test: Buscar post por ID."""
    repo = PostSqlRepository(db_client)
    
    # Creamos un post
    repo.create("First Post", "Content", 1)
    
    # Buscamos por ID
    post = repo.get_by_id(1)
    assert post is not None
    assert post.title == "First Post"
    
    # Buscamos ID inexistente
    not_found = repo.get_by_id(999)
    assert not_found is None


def test_post_repository_update(db_client):
    """Test: Actualizar un post."""
    repo = PostSqlRepository(db_client)
    
    # Creamos y actualizamos
    repo.create("Original", "Content", 1)
    repo.update(1, "Updated Title", "Updated Content")
    
    # Verificamos
    post = repo.get_by_id(1)
    assert post.title == "Updated Title"
    assert post.content == "Updated Content"


def test_post_repository_delete(db_client):
    """Test: Eliminar un post."""
    repo = PostSqlRepository(db_client)
    
    # Creamos y eliminamos
    repo.create("To Delete", "Content", 1)
    repo.delete(1)
    
    # Verificamos que ya no existe
    assert repo.get_by_id(1) is None
    assert len(repo.get_all()) == 0
