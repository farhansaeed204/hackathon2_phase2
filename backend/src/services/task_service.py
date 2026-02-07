from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.task import Task, TaskCreate, TaskUpdate
from src.core.database import get_session
from uuid import UUID, uuid4


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_data: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for a specific user
        """
        task = Task.from_orm(task_data)
        task.user_id = user_id  # Assign the user_id to ensure proper isolation
        
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        
        return task

    async def get_task_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for a specific user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)
        task = result.first()
        return task

    async def get_tasks_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all tasks for a specific user with pagination
        """
        statement = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        tasks = result.all()
        return tasks

    async def update_task(self, task_id: str, task_data: TaskUpdate, user_id: str) -> Optional[Task]:
        """
        Update a specific task for a specific user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)
        task = result.first()

        if task:
            # Update only the fields that are provided in task_data
            update_data = task_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(task, field, value)
            
            task.updated_at = task.updated_at.__class__()  # Update the timestamp
            
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)
            
            return task
        
        return None

    async def delete_task(self, task_id: str, user_id: str) -> bool:
        """
        Delete a specific task for a specific user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)
        task = result.first()

        if task:
            await self.session.delete(task)
            await self.session.commit()
            return True
        
        return False

    async def toggle_task_completion(self, task_id: str, user_id: str) -> Optional[Task]:
        """
        Toggle the completion status of a specific task for a specific user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)
        task = result.first()

        if task:
            task.completed = not task.completed
            task.updated_at = task.updated_at.__class__()  # Update the timestamp
            
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)
            
            return task
        
        return None