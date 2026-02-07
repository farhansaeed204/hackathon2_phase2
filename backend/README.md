# Task Management Backend API

This is a FastAPI backend for managing tasks with user authentication and authorization. It uses SQLModel with Neon Postgres as the database.

## Features

- Full CRUD operations for tasks
- User-specific task management
- JWT-based authentication
- Async database operations
- Proper error handling
- CORS support for frontend integration

## Endpoints

All endpoints follow the pattern: `/api/{user_id}/tasks/`

- `GET /{user_id}/tasks/` - Get all tasks for a user
- `POST /{user_id}/tasks/` - Create a new task
- `GET /{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /{user_id}/tasks/{task_id}` - Update a specific task
- `DELETE /{user_id}/tasks/{task_id}` - Delete a specific task
- `PATCH /{user_id}/tasks/{task_id}/toggle_complete` - Toggle task completion status

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Update the `.env` file with your actual database URL and JWT secret.

4. Run the application:
```bash
uvicorn main:app --reload
```

## Environment Variables

- `NEON_DB_URL`: Your Neon Postgres database connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing