# FastAPI Simple Architecture

API REST construida con FastAPI utilizando una arquitectura hexagonal (Ports and Adapters).

## Tabla de Contenidos

- [Descripción](#descripción)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelos de Dominio](#modelos-de-dominio)
- [Servicios de Aplicación](#servicios-de-aplicación)
- [Repositorios](#repositorios)
- [API Endpoints](#api-endpoints)
- [Autenticación](#autenticación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)

## Descripción

API RESTful para gestión de usuarios y posts con autenticación JWT. Soporta PostgreSQL y SQLite.

## Arquitectura

El proyecto sigue el patrón **Hexagonal** (Ports and Adapters):

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Routers    │  │    DTOs     │  │  Response Handlers      │ │
│  │  (API)      │  │             │  │                         │ │
│  └──────┬──────┘  └─────────────┘  └─────────────────────────┘ │
└─────────┼───────────────────────────────────────────────────────┘
          │
┌─────────┼───────────────────────────────────────────────────────┐
│         │               APPLICATION LAYER                      │
│  ┌──────▼──────────────────────────────────────┐  ┌───────────┐ │
│  │              Services                        │  │   Ports   │ │
│  │  - UserService                              │  │ (Interfaces│ │
│  │  - PostService                              │  │  Abtractas)│ │
│  │  - AuthService                              │  └─────┬─────┘ │
│  └─────────────────────────────────────────────┘        │       │
└──────────────────────────────────────────────────────────┼───────┘
                                                           │
┌──────────────────────────────────────────────────────────┼───────┐
│                         DOMAIN LAYER                      │       │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────▼─────┐ │
│  │   Entities     │  │   Exceptions    │  │      Enums         │ │
│  │  - UserModel   │  │  - AppError     │  │   - RoleEnum       │ │
│  │  - PostModel   │  │  - NotFoundError│  │                    │ │
│  │  - RoleModel   │  │  - etc.         │  │                    │ │
│  └────────────────┘  └────────────────┘  └────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
          │
┌─────────┼───────────────────────────────────────────────────────┐
│         │              INFRASTRUCTURE LAYER                     │
│  ┌──────▼──────────────────────────────────────────────────────┐│
│  │              Adapters (Implementaciones concretas)           ││
│  │  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐  ││
│  │  │  Repositories  │  │  DB Clients    │  │    Mappers    │  ││
│  │  │  - UserSqlRepo │  │  - Postgres    │  │  - UserMapper │  ││
│  │  │  - PostSqlRepo │  │  - Sqlite      │  │  - PostMapper │  ││
│  │  │  - RoleSqlRepo │  │                │  │               │  ││
│  │  └────────────────┘  └────────────────┘  └───────────────┘  ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### Capas

1. **Domain**: Entidades y lógica de negocio pura
2. **Application**: Servicios y puertos (interfaces)
3. **Infrastructure**: Implementaciones concretas (repositories, db clients)
4. **Presentation**: Routers, DTOs, responses

## Estructura del Proyecto

```
app/
├── domain/
│   ├── entities/
│   │   ├── user.py          # UserModel
│   │   ├── post.py          # PostModel
│   │   └── role.py          # RoleModel
│   ├── enums/
│   │   └── role.py          # RoleEnum (ADMIN, USER)
│   └── exceptions.py        # Excepciones personalizadas
├── application/
│   ├── ports/               # Interfaces abstratas
│   │   ├── user_repository_port.py
│   │   ├── post_repository_port.py
│   │   ├── role_repository_port.py
│   │   └── db_client_port.py
│   └── services/            # Lógica de negocio
│       ├── user_service.py
│       ├── post_service.py
│       └── auth_service.py
├── infrastructure/
│   └── adapters/
│       ├── db/
│       │   └── clients/
│       │       ├── postgres_client.py
│       │       └── sqlite_client.py
│       ├── repositories/
│       │   ├── user_sql_repository.py
│       │   ├── post_sql_repository.py
│       │   └── role_sql_repository.py
│       └── mappers/
│           ├── user_mapper.py
│           └── post_mapper.py
└── presentation/
    ├── api/
    │   ├── user_router.py
    │   ├── post_router.py
    │   └── auth_router.py
    ├── dto/
    │   ├── create_user_dto.py
    │   ├── update_user_dto.py
    │   ├── create_post_dto.py
    │   ├── update_post_dto.py
    │   ├── register_user_dto.py
    │   └── login_dto.py
    ├── dependencies/
    │   └── deps.py          # Inyección de dependencias
    └── response.py          # ApiResponse wrapper
```

## Modelos de Dominio

### UserModel
```python
@dataclass
class UserModel:
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
    date_of_birth: str
    role_id: int
```

### PostModel
```python
class PostModel(BaseModel):
    id: int
    title: str
    content: str
    userId: int
    created_at: datetime
    updated_at: datetime
```

### RoleModel
```python
@dataclass
class RoleModel:
    id: int
    name: str
    description: str
```

### RoleEnum
```python
class RoleEnum(Enum):
    ADMIN = 1
    USER = 2
```

## Servicios de Aplicación

### UserService
Gestiona operaciones CRUD de usuarios.

### PostService
Gestiona operaciones CRUD de posts con validación de usuario existente.

### AuthService
- `get_password_hash()`: Genera hash bcrypt de contraseña
- `verify_password()`: Verifica contraseña contra hash
- `create_access_token()`: Crea token JWT
- `decode_access_token()`: Decodifica token JWT
- `verify_token_payload()`: Valida payload del token

## Repositorios

Implementaciones de puertos abstratos:

| Puerto | Implementación |
|--------|---------------|
| UserRepositoryPort | UserSqlRepository |
| PostRepositoryPort | PostSqlRepository |
| RoleRepositoryPort | RoleSqlRepository |
| DbClientPort | PostgresClient / SqliteClient |

## API Endpoints

### Autenticación (`/auth`)

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/register` | Registrar nuevo usuario |
| POST | `/auth/login` | Iniciar sesión |
| POST | `/auth/token` | OAuth2 token (para Swagger) |

### Usuarios (`/users`)

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/users/` | Admin | Listar todos los usuarios |
| POST | `/users/` | Admin | Crear usuario |
| GET | `/users/{user_id}` | User | Obtener usuario por ID |
| PUT | `/users/{user_id}` | User | Actualizar usuario |
| DELETE | `/users/{user_id}` | Admin | Eliminar usuario |

### Posts (`/posts`)

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/posts/` | - | Listar todos los posts |
| POST | `/posts/` | - | Crear post |
| GET | `/posts/{post_id}` | - | Obtener post por ID |
| PUT | `/posts/{post_id}` | - | Actualizar post |
| DELETE | `/posts/{post_id}` | - | Eliminar post |

## Autenticación

### JWT Token

- **Algoritmo**: HS256
- **Expiración**: 30 minutos
- **Payload**: `{ "sub": email, "user_id": int, "role_id": int }`

### Roles

| Rol | ID | Permisos |
|-----|----|----------|
| Admin | 1 | CRUD completo de usuarios y posts |
| User | 2 | Lectura/actualización de su perfil, CRUD de posts |

### Uso

```bash
# Login para obtener token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@admin.com", "password": "borntofeel"}'

# Usar token en requests
curl -X GET http://localhost:8000/users/ \
  -H "Authorization: Bearer <token>"
```

## DTOs

### User DTOs

- **CreateUserDto**: first_name, last_name, email, password (min 6), date_of_birth
- **UpdateUserDto**: first_name, last_name, email, date_of_birth
- **RegisterUserDto**: Igual que CreateUserDto

Validaciones:
- Email debe contener `@`
- Usuario debe ser mayor de 18 años

### Post DTOs

- **CreatePostDto**: title (1-255 chars), content, user_id
- **UpdatePostDto**: title (1-255 chars), content

### Auth DTOs

- **LoginDto**: email, password

## Excepciones

| Excepción | Status | Código |
|-----------|--------|--------|
| NotFoundError | 404 | NOT_FOUND |
| BadRequestError | 400 | BAD_REQUEST |
| ConflictError | 409 | CONFLICT |
| UnauthorizedError | 401 | UNAUTHORIZED |
| ForbiddenError | 403 | FORBIDDEN |
| ServerError | 500 | SERVER_ERROR |

## Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| DATABASE_URL | Connection string PostgreSQL | SQLite local |

### Base de Datos

Por defecto usa SQLite (`database.db`). Para PostgreSQL:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db
```

#### Inicializar Base de Datos

```bash
python init_db.py
```

## Ejecución

### Con Docker (PostgreSQL)

```bash
docker-compose up -d
python init_db.py
uvicorn main:app --reload
```

### Sin Docker (SQLite)

```bash
python init_db.py
uvicorn main:app --reload
```

### Acceso

- **API**: http://localhost:8000
- **Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Usuario Admin Default

```
Email: admin@admin.com
Password: borntofeel
```
