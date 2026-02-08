from sqlmodel import SQLModel, create_engine
from backend.models.task import Task
import os

DATABASE_URL = os.getenv("NEON_DB_URL")

engine = create_engine(DATABASE_URL, echo=True)

async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)