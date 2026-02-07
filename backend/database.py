from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("NEON_DB_URL", "")

# Sync engine for table creation
engine = create_engine(DATABASE_URL)

# Async engine for async operations
async_engine = create_async_engine(DATABASE_URL)

# Async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session
    """
    async with AsyncSessionLocal() as session:
        yield session