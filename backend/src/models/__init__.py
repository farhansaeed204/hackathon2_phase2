from sqlmodel import SQLModel
from .user import User
from .task import Task

# This file serves as the base for all models
# All models will inherit from SQLModel

__all__ = ["SQLModel", "User", "Task"]