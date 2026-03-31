"""
Tests for Application Layer - Services (with Mocks)

La capa de aplicación contiene la lógica de negocio.
Usamos MOCKS de los repositorios para NO depender de la base de datos.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock

from app.application.services.post_service import PostService
from app.domain.entities.post import PostModel
from app.domain.entities.user import UserModel
from app.domain.exceptions import NotFoundError


def test_get_all_posts():
    """Test: Obtener todos los posts."""
    # Arrange: Creamos mocks de los repositorios
    mock_post_repo = Mock()
    mock_user_repo = Mock()
    
    # Configuramos el mock para devolver datos de prueba
    mock_post_repo.get_all.return_value = [
        PostModel(id=1, title="Post 1", content="Content 1", userId=1, 
                  created_at=datetime.now(), updated_at=datetime.now()),
        PostModel(id=2, title="Post 2", content="Content 2", userId=1,
                  created_at=datetime.now(), updated_at=datetime.now()),
    ]
    
    # Act: Creamos el servicio con los mocks
    service = PostService(mock_post_repo, mock_user_repo)
    result = service.get_all()
    
    # Assert: Verificamos
    assert len(result) == 2
    assert result[0].title == "Post 1"
    mock_post_repo.get_all.assert_called_once()  # Verificamos que se llamó al repo


def test_create_post_success():
    """Test: Crear un post cuando el usuario existe."""
    # Arrange
    mock_post_repo = Mock()
    mock_user_repo = Mock()
    
    # Simulamos que el usuario existe
    mock_user_repo.get_by_id.return_value = UserModel(
        id=1, first_name="John", last_name="Doe", email="john@example.com",
        password="pass", date_of_birth="1990-01-01", role_id=1
    )
    
    service = PostService(mock_post_repo, mock_user_repo)
    
    # Act
    service.create("New Post", "Content", 1)
    
    # Assert
    mock_user_repo.get_by_id.assert_called_once_with(1)  # Verificó el usuario
    mock_post_repo.create.assert_called_once_with("New Post", "Content", 1)  # Creó el post


def test_create_post_user_not_found():
    """Test: Crear post cuando el usuario NO existe (debe fallar)."""
    # Arrange
    mock_post_repo = Mock()
    mock_user_repo = Mock()
    
    # Simulamos que el usuario NO existe
    mock_user_repo.get_by_id.return_value = None
    
    service = PostService(mock_post_repo, mock_user_repo)
    
    # Act & Assert
    with pytest.raises(NotFoundError) as exc_info:
        service.create("New Post", "Content", 999)
    
    assert exc_info.value.code == "USER_NOT_FOUND"
    assert "User not found" in str(exc_info.value)


def test_update_post_not_found():
    """Test: Actualizar un post que no existe."""
    # Arrange
    mock_post_repo = Mock()
    mock_user_repo = Mock()
    
    mock_post_repo.get_by_id.return_value = None
    
    service = PostService(mock_post_repo, mock_user_repo)
    
    # Act & Assert
    with pytest.raises(NotFoundError) as exc_info:
        service.update(999, "Updated Title", "Updated Content")
    
    assert exc_info.value.code == "POST_NOT_FOUND"
