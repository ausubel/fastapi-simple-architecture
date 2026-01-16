import pytest
from datetime import date

def test_register_user_success(client):
    payload = {
        "first_name": "Integration",
        "last_name": "User",
        "email": "integration@test.com",
        "password": "strongPassword123",
        "date_of_birth": "1990-01-01"
    }
    
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User registered successfully"

def test_login_success(client):
    # First register
    payload = {
        "first_name": "Login",
        "last_name": "User",
        "email": "login@test.com",
        "password": "password123",
        "date_of_birth": "1990-05-05"
    }
    client.post("/auth/register", json=payload)
    
    # Login
    login_payload = {
        "email": "login@test.com",
        "password": "password123"
    }
    
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]

def test_login_invalid_credentials(client):
     # First register
    payload = {
        "first_name": "Wrong",
        "last_name": "Pass",
        "email": "wrong@test.com",
        "password": "password123",
        "date_of_birth": "1990-05-05"
    }
    client.post("/auth/register", json=payload)

    login_payload = {
        "email": "wrong@test.com",
        "password": "wrongpassword"
    }
    
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 401
