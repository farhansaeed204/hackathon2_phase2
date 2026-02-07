from fastapi import Request, HTTPException, status
from typing import Callable, Awaitable
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "")
ALGORITHM = "HS256"


async def jwt_middleware(request: Request, call_next: Callable[[Request], Awaitable]):
    """
    Middleware to verify JWT token in Authorization header for protected routes
    """
    # Define paths that don't require authentication
    public_paths = ["/", "/docs", "/redoc", "/openapi.json", "/health"]
    
    # Check if the path is public
    is_public_route = any(request.url.path.startswith(path) for path in public_paths)
    
    # If it's not a public route, require authorization
    if not is_public_route:
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid format"
            )
        
        token = auth_header.split(" ")[1]
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
            
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )
            
            # Add user_id to request state for use in route handlers
            request.state.user_id = user_id
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
    
    response = await call_next(request)
    return response