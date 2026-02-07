import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.task_service import TaskService
from src.models.task import Task, TaskCreate, TaskUpdate
from uuid import uuid4


@pytest.mark.asyncio
async def test_create_task():
    """Test creating a task"""
    # Arrange
    session_mock = AsyncMock()
    task_service = TaskService(session_mock)
    
    user_id = str(uuid4())
    task_create_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False
    )
    
    # Act
    result = await task_service.create_task(task_create_data, user_id)
    
    # Assert
    assert result is not None
    assert result.title == "Test Task"
    assert result.description == "Test Description"
    assert result.user_id == user_id
    assert result.completed is False
    session_mock.add.assert_called_once()
    session_mock.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_task_by_id():
    """Test getting a task by ID for a specific user"""
    # Arrange
    session_mock = AsyncMock()
    task_service = TaskService(session_mock)
    
    task_id = str(uuid4())
    user_id = str(uuid4())
    
    # Mock the query result
    mock_task = Task(
        id=task_id,
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id=user_id
    )
    execute_result = MagicMock()
    execute_result.first.return_value = mock_task
    session_mock.execute.return_value = execute_result
    
    # Act
    result = await task_service.get_task_by_id(task_id, user_id)
    
    # Assert
    assert result == mock_task
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_tasks_by_user():
    """Test getting all tasks for a specific user"""
    # Arrange
    session_mock = AsyncMock()
    task_service = TaskService(session_mock)
    
    user_id = str(uuid4())
    
    # Mock the query result
    mock_tasks = [
        Task(id=str(uuid4()), title="Task 1", description="Desc 1", completed=False, user_id=user_id),
        Task(id=str(uuid4()), title="Task 2", description="Desc 2", completed=True, user_id=user_id)
    ]
    execute_result = MagicMock()
    execute_result.all.return_value = mock_tasks
    session_mock.execute.return_value = execute_result
    
    # Act
    result = await task_service.get_tasks_by_user(user_id)
    
    # Assert
    assert len(result) == 2
    assert result[0].title == "Task 1"
    assert result[1].title == "Task 2"
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_task():
    """Test updating a task"""
    # Arrange
    session_mock = AsyncMock()
    task_service = TaskService(session_mock)
    
    task_id = str(uuid4())
    user_id = str(uuid4())
    
    # Mock the existing task
    existing_task = Task(
        id=task_id,
        title="Old Title",
        description="Old Description",
        completed=False,
        user_id=user_id
    )
    execute_result = MagicMock()
    execute_result.first.return_value = existing_task
    session_mock.execute.return_value = execute_result
    
    # Prepare update data
    task_update_data = TaskUpdate(
        title="New Title",
        completed=True
    )
    
    # Act
    result = await task_service.update_task(task_id, task_update_data, user_id)
    
    # Assert
    assert result is not None
    assert result.title == "New Title"
    assert result.completed is True
    assert result.description == "Old Description"  # Should remain unchanged
    session_mock.add.assert_called_once()
    session_mock.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task():
    """Test deleting a task"""
    # Arrange
    session_mock = AsyncMock()
    task_service = TaskService(session_mock)
    
    task_id = str(uuid4())
    user_id = str(uuid4())
    
    # Mock the existing task
    existing_task = Task(
        id=task_id,
        title="Task to Delete",
        description="Description",
        completed=False,
        user_id=user_id
    )
    execute_result = MagicMock()
    execute_result.first.return_value = existing_task
    session_mock.execute.return_value = execute_result
    
    # Act
    result = await task_service.delete_task(task_id, user_id)
    
    # Assert
    assert result is True
    session_mock.delete.assert_called_once_with(existing_task)
    session_mock.commit.assert_called_once()


@pytest.mark.asyncio
async def test_toggle_task_completion():
    """Test toggling task completion status"""
    # Arrange
    session_mock = AsyncMock()
    task_service = TaskService(session_mock)
    
    task_id = str(uuid4())
    user_id = str(uuid4())
    
    # Mock the existing task (initially not completed)
    existing_task = Task(
        id=task_id,
        title="Task to Toggle",
        description="Description",
        completed=False,  # Initially False
        user_id=user_id
    )
    execute_result = MagicMock()
    execute_result.first.return_value = existing_task
    session_mock.execute.return_value = execute_result
    
    # Act
    result = await task_service.toggle_task_completion(task_id, user_id)
    
    # Assert
    assert result is not None
    assert result.completed is True  # Should now be True
    session_mock.add.assert_called_once()
    session_mock.commit.assert_called_once()