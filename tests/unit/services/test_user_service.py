import pytest
from unittest.mock import MagicMock
from datetime import date
from app.services.user_service import UserService
from app.repository.user_repository import UserRepository
from app.repository.models.user_model import UserModel

def test_create_user_calls_repository():
    # Arrange
    mock_repo = MagicMock(spec=UserRepository)
    service = UserService(mock_repo)
    dob = date(1990, 1, 1)
    
    # Act
    service.create("John", "Doe", "test@example.com", "pass", dob)
    
    # Assert
    mock_repo.create.assert_called_once_with("John", "Doe", "test@example.com", "pass", dob)

def test_get_by_id_returns_user():
    # Arrange
    mock_repo = MagicMock(spec=UserRepository)
    expected_user = UserModel(
        id=1, 
        first_name="John", 
        last_name="Doe", 
        email="test@example.com", 
        password="pass", 
        date_of_birth="1990-01-01", 
        role_id=1
    )
    mock_repo.get_by_id.return_value = expected_user
    service = UserService(mock_repo)
    
    # Act
    result = service.get_by_id(1)
    
    # Assert
    assert result == expected_user
    mock_repo.get_by_id.assert_called_once_with(1)
