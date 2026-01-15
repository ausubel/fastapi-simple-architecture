from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.services.auth_service import AuthService
from app.shared.role_enum import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class UserTokenPayload(BaseModel):
    user_id: int
    email: str
    role_id: int

def get_auth_service():
    return AuthService()

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserTokenPayload:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = auth_service.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    user_id: int = payload.get("user_id")
    role_id: int = payload.get("role_id")

    if email is None or user_id is None or role_id is None:
        raise credentials_exception
        
    return UserTokenPayload(
        user_id=user_id,
        email=email,
        role_id=role_id
    )

def get_current_admin(
    current_user: Annotated[UserTokenPayload, Depends(get_current_user)]
) -> UserTokenPayload:
    if current_user.role_id != RoleEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
