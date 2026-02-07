from fastapi import Depends, HTTPException, status, Request
from typing import Optional
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "")
ALGORITHM = "HS256"


def verify_jwt_token(token: str):
    """
    Verify the JWT token and return the payload
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


async def verify_user_id(user_id: int, request: Request) -> int:
    """
    Extract and verify user_id from JWT token in Authorization header
    """
    # Get the Authorization header
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid format"
        )
    
    # Extract the token
    token = auth_header.split(" ")[1]
    
    # Verify the token and get the payload
    payload = verify_jwt_token(token)
    
    # Verify that the user_id in the path matches the user_id in the token
    token_user_id = payload.get("user_id")
    
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user ID mismatch"
        )
    
    return user_id