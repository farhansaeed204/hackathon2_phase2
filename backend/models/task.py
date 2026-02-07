from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class TaskBase(SQLModel):
    """
    Base model for Task with common fields
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: int  # We'll handle the foreign key relationship differently


class Task(TaskBase, table=True):
    """
    Task model representing the tasks table in the database
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskResponse(TaskBase):
    """
    Response model for Task API
    """
    id: int
    created_at: datetime
    updated_at: datetime