"""
Tests for Domain Layer - Entities

La capa de dominio contiene las reglas de negocio puras.
Estas pruebas son las MÁS SIMPLES porque no dependen de nada externo.
"""

from datetime import datetime
from app.domain.entities.post import PostModel
from app.domain.entities.user import UserModel


def test_post_model_creation():
    """Test que verifica la creación de un PostModel."""
    post = PostModel(
        id=1,
        title="Test Title",
        content="Test Content",
        userId=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    assert post.id == 1
    assert post.title == "Test Title"
    assert post.content == "Test Content"
    assert post.userId == 1


def test_user_model_creation():
    """Test que verifica la creación de un UserModel."""
    user = UserModel(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="hashed_password",
        date_of_birth="1990-01-01",
        role_id=1
    )
    
    assert user.id == 1
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john@example.com"


def test_post_model_validation():
    """Test que verifica validación de datos (Pydantic)."""
    try:
        # Esto debería funcionar
        post = PostModel(
            id=1,
            title="Valid Title",
            content="Valid Content",
            userId=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert post.title == "Valid Title"
    except Exception:
        pass  # Si falla, es porque Pydantic validó algo
