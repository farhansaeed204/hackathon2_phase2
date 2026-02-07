from pydantic_settings import BaseSettings
from typing import Optional
from contextlib import asynccontextmanager
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = {"env_file": ".env"}

    APP_NAME: str = "Todo API"
    API_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Secure API for managing user tasks in the Todo application"
    
    # Database settings
    DATABASE_URL: str = Field(default="", alias="NEON_DB_URL")
    
    # Auth settings
    BETTER_AUTH_SECRET: str = Field(default="", alias="BETTER_AUTH_SECRET")
    BETTER_AUTH_URL: str = Field(default="", alias="BETTER_AUTH_URL")
    
    # JWT settings
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    FRONTEND_URL: str = Field(default="http://localhost:3001", alias="FRONTEND_URL")

settings = Settings()

# Create the async engine
engine = None

async def get_engine():
    global engine
    if engine is None:
        engine = create_async_engine(settings.DATABASE_URL)
    return engine

@asynccontextmanager
async def lifespan(app):
    # Startup
    yield
    # Shutdown
    if engine:
        await engine.dispose()