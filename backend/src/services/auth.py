"""
Authentication service module for handling JWT verification and user context extraction.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
from src.core.config import settings

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: Optional[str] = None

def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify the JWT token and extract user_id from it
    """
    try:
        payload = jwt.decode(
            token, 
            settings.BETTER_AUTH_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Extract user_id from the token
        user_id: str = payload.get("userId") or payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        token_data = TokenData(user_id=user_id)
        return token_data
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get the current user from the JWT token
    """
    token_data = verify_token(credentials.credentials)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data.user_id