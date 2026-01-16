import pytest
from datetime import date
from app.repository.user_repository import UserRepository

def test_create_and_get_user(test_db_client):
    # Initialize repository with the test DB client
    repo = UserRepository(test_db_client)
    
    dob = date(1990, 1, 1)
    email = "john.doe@example.com"
    
    # Act: Create user
    repo.create("John", "Doe", email, "secret123", dob)
    
    # Assert: Get by Email
    user = repo.get_by_email(email)
    assert user is not None
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == email
    assert user.date_of_birth == dob.strftime("%Y-%m-%d")

    # Assert: Get by ID
    user_by_id = repo.get_by_id(user.id)
    assert user_by_id is not None
    assert user_by_id.email == email

def test_update_user(test_db_client):
    repo = UserRepository(test_db_client)
    dob = date(1990, 1, 1)
    email = "update@example.com"
    
    repo.create("Jane", "Doe", email, "pass", dob)
    user = repo.get_by_email(email)
    
    # Act: Update
    new_dob = date(1991, 2, 2)
    repo.update(user.id, "JaneUpdated", "DoeUpdated", "new@example.com", new_dob)
    
    # Assert
    updated = repo.get_by_id(user.id)
    assert updated.first_name == "JaneUpdated"
    assert updated.email == "new@example.com"
    assert updated.date_of_birth == new_dob.strftime("%Y-%m-%d")

def test_delete_user(test_db_client):
    repo = UserRepository(test_db_client)
    dob = date(1990, 1, 1)
    email = "delete@example.com"
    
    repo.create("Delete", "Me", email, "pass", dob)
    user = repo.get_by_email(email)
    assert user is not None
    
    # Act: Delete
    repo.delete(user.id)
    
    # Assert
    deleted = repo.get_by_id(user.id)
    assert deleted is None
