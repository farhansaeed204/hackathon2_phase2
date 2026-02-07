from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router
from src.core.config import settings
from contextlib import asynccontextmanager
from src.core.config import lifespan
from src.core.database import get_session
from src.services.auth import get_current_user

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address)

# Create the FastAPI application with lifespan
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan
)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth and task routers
app.include_router(auth_router, tags=["auth"])
app.include_router(tasks_router, prefix="/api/{user_id}", tags=["tasks"])


# Custom middleware to add security headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # Add security headers to all responses
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


# Add the security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}