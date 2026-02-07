import pytest
from httpx import AsyncClient
from jose import jwt
from src.core.config import settings
from src.models.task import TaskCreate


@pytest.mark.asyncio
async def test_create_task_endpoint(client, db_session):
    """Test creating a task via the API endpoint"""
    # Create a valid token
    test_user_id = "test_user_123"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Prepare task data
    task_data = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    
    # Make a request to create a task
    response = await client.post(
        f"/api/{test_user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert the response
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["user_id"] == test_user_id
    assert data["completed"] is False


@pytest.mark.asyncio
async def test_get_task_endpoint(client, db_session):
    """Test getting a specific task via the API endpoint"""
    # Create a valid token
    test_user_id = "test_user_456"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # First, create a task
    task_data = {
        "title": "Get Test Task",
        "description": "This is a test task for getting"
    }
    create_response = await client.post(
        f"/api/{test_user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Now, get the task
    response = await client.get(
        f"/api/{test_user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert the response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Test Task"


@pytest.mark.asyncio
async def test_get_all_tasks_endpoint(client, db_session):
    """Test getting all tasks for a user via the API endpoint"""
    # Create a valid token
    test_user_id = "test_user_789"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Create multiple tasks
    for i in range(3):
        task_data = {
            "title": f"Task {i}",
            "description": f"This is test task {i}"
        }
        create_response = await client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert create_response.status_code == 200
    
    # Get all tasks
    response = await client.get(
        f"/api/{test_user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    titles = [task["title"] for task in data]
    assert "Task 0" in titles
    assert "Task 1" in titles
    assert "Task 2" in titles


@pytest.mark.asyncio
async def test_update_task_endpoint(client, db_session):
    """Test updating a task via the API endpoint"""
    # Create a valid token
    test_user_id = "test_user_101"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # First, create a task
    task_data = {
        "title": "Original Task",
        "description": "Original description"
    }
    create_response = await client.post(
        f"/api/{test_user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Now, update the task
    update_data = {
        "title": "Updated Task",
        "completed": True
    }
    response = await client.put(
        f"/api/{test_user_id}/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert the response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Task"
    assert data["completed"] is True


@pytest.mark.asyncio
async def test_delete_task_endpoint(client, db_session):
    """Test deleting a task via the API endpoint"""
    # Create a valid token
    test_user_id = "test_user_202"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # First, create a task
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted"
    }
    create_response = await client.post(
        f"/api/{test_user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Now, delete the task
    response = await client.delete(
        f"/api/{test_user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert the response
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"


@pytest.mark.asyncio
async def test_toggle_task_completion_endpoint(client, db_session):
    """Test toggling task completion via the API endpoint"""
    # Create a valid token
    test_user_id = "test_user_303"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # First, create a task
    task_data = {
        "title": "Task to Toggle",
        "description": "This task completion will be toggled",
        "completed": False
    }
    create_response = await client.post(
        f"/api/{test_user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]
    assert created_task["completed"] is False
    
    # Now, toggle the task completion
    response = await client.patch(
        f"/api/{test_user_id}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert the response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["completed"] is True  # Should now be True


@pytest.mark.asyncio
async def test_task_endpoints_unauthorized_access(client, db_session):
    """Test that accessing task endpoints without proper authorization returns 401"""
    test_user_id = "test_user_404"
    
    # Try to create a task without a token
    task_data = {
        "title": "Unauthorized Task",
        "description": "This should fail"
    }
    response = await client.post(
        f"/api/{test_user_id}/tasks",
        json=task_data
    )
    
    # Assert the response is 401 Unauthorized
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_task_not_found(client, db_session):
    """Test that accessing a non-existent task returns 404"""
    # Create a valid token
    test_user_id = "test_user_505"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Try to get a non-existent task
    fake_task_id = "non_existent_task_id"
    response = await client.get(
        f"/api/{test_user_id}/tasks/{fake_task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert the response is 404 Not Found
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]