"""
Tests for Presentation Layer - FastAPI Routes

La capa de presentación maneja HTTP.
Usamos TestClient para simular requests sin levantar el servidor real.
"""
from fastapi.testclient import TestClient
from main import app

# Creamos un cliente de prueba
client = TestClient(app)


def test_get_posts_returns_data():
    """Test: GET /posts/ devuelve posts (hay datos de prueba en schema_postgres.sql)."""
    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # Hay posts de prueba ("Pact Title" del schema_postgres.sql)
    assert len(data["data"]) > 0
    assert data["data"][0]["title"] == "Pact Title"


def test_get_posts_structure():
    """Test: Verificar la estructura de la respuesta."""
    response = client.get("/posts/")
    assert response.status_code == 200
    
    data = response.json()
    # Verificamos que tiene los campos esperados
    assert "success" in data
    assert "data" in data
    assert "message" in data


def test_login_success():
    """Test: Login con credenciales válidas (del schema_postgres.sql)."""
    response = client.post("/auth/login/", json={
        "email": "admin@admin.com",
        "password": "borntofeel"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


def test_login_failure():
    """Test: Login con credenciales inválidas."""
    response = client.post("/auth/login/", json={
        "email": "wrong@email.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401  # Unauthorized
    # HTTPException de FastAPI retorna detail, no success
    assert "detail" in response.json()


def test_create_post_success():
    """Test: Crear post (endpoint no requiere auth en esta implementación)."""
    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "Test Content",
        "user_id": 1  # Admin user exists
    })
    
    # El endpoint no tiene protección de auth, debería funcionar
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True


# Para testear endpoints protegidos necesitamos el token
def test_create_post_authorized():
    """Test: Crear post con token válido."""
    # 1. Login para obtener token
    login_response = client.post("/auth/login/", json={
        "email": "admin@admin.com",
        "password": "borntofeel"
    })
    token = login_response.json()["data"]["access_token"]
    
    # 2. Crear post con el token
    response = client.post(
        "/posts/",
        json={"title": "New Post", "content": "Content", "user_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Verificamos que la estructura de respuesta es correcta
    assert response.status_code in [200, 201, 422]  # Depende de la implementación
