from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import os
from pathlib import Path

from app.application.services.auth_service import AuthService
from app.application.services.user_service import UserService
from app.application.services.post_service import PostService
from app.domain.exceptions import UnauthorizedError
from app.domain.enums.role import RoleEnum

from app.application.ports.db_client_port import DbClientPort

from app.infrastructure.adapters.db.clients.postgres_client import PostgresClient
from app.infrastructure.adapters.db.clients.sqlite_client import SqliteClient
from app.infrastructure.adapters.repositories.user_sql_repository import (
    UserSqlRepository,
)
from app.infrastructure.adapters.repositories.post_sql_repository import (
    PostSqlRepository,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class UserTokenPayload(BaseModel):
    user_id: int
    email: str
    role_id: int


def get_db_client() -> DbClientPort:
    dsn = os.getenv("DATABASE_URL")
    if dsn:
        return PostgresClient.get_instance(dsn)
    db_path = Path.cwd() / "database.db"
    return SqliteClient.get_instance(db_path)


DbClientDep = Annotated[DbClientPort, Depends(get_db_client)]


def get_auth_service():
    return AuthService()


def get_user_service(db: DbClientDep) -> UserService:
    repo = UserSqlRepository(db)
    return UserService(repo)


def get_post_service(db: DbClientDep) -> PostService:
    post_repo = PostSqlRepository(db)
    user_repo = UserSqlRepository(db)
    return PostService(post_repo, user_repo)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserTokenPayload:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = auth_service.verify_token_payload(token)
        return UserTokenPayload(**payload)
    except UnauthorizedError:
        raise credentials_exception


def get_current_admin(
    current_user: Annotated[UserTokenPayload, Depends(get_current_user)],
) -> UserTokenPayload:
    if current_user.role_id != RoleEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
