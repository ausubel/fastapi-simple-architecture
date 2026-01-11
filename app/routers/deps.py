from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.db.dependencies import LocalDb
from app.repository.user_repository import UserRepository
from app.shared.role_enum import RoleEnum
from app.repository.models.user_model import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_auth_service():
    return AuthService()

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: LocalDb,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserModel:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = auth_service.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    user_repository = UserRepository(session)
    user_service = UserService(user_repository)
    user = user_service.get_by_email(email)
    
    if user is None:
        raise credentials_exception
        
    return user

def get_current_admin(
    current_user: Annotated[UserModel, Depends(get_current_user)]
) -> UserModel:
    if current_user.role_id != RoleEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
