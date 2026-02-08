from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

security = HTTPBearer()
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")

class JWTAuth:
    def __init__(self):
        self.secret_key = SECRET_KEY
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await security(request)
        try:
            token = credentials.credentials
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
            
            request.state.user_id = user_id
        except jwt.JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
        
        return request