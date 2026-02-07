# Todo API Backend

This is the backend API for the Todo Full-Stack Web Application. It provides secure API endpoints for task management operations using FastAPI, SQLModel, and Neon Postgres.

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Postgres
- **Authentication**: JWT with Better Auth
- **Rate Limiting**: SlowAPI
- **Testing**: pytest

## Setup Instructions

1. Clone the repository
2. Navigate to the backend directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy the environment file and fill in your values:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```
6. Run database migrations:
   ```bash
   alembic upgrade head
   ```
7. Start the development server:
   ```bash
   uvicorn src.main:app --reload
   ```

## Environment Variables

- `NEON_DB_URL`: Your Neon Postgres database connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT verification
- `BETTER_AUTH_URL`: Better Auth instance URL
- `FRONTEND_URL`: URL of the frontend application (default: http://localhost:3000)

## API Endpoints

All endpoints require a valid JWT token in the Authorization header: `Authorization: Bearer <token>`

- `GET /api/{user_id}/tasks` - List user's tasks (Rate limit: 20/min)
- `POST /api/{user_id}/tasks` - Create new task (Rate limit: 10/min)
- `GET /api/{user_id}/tasks/{id}` - Get specific task (Rate limit: 20/min)
- `PUT /api/{user_id}/tasks/{id}` - Update task (Rate limit: 15/min)
- `DELETE /api/{user_id}/tasks/{id}` - Delete task (Rate limit: 10/min)
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion (Rate limit: 15/min)

### Security Headers

All API responses include the following security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

### Rate Limits

The API implements rate limiting per IP address:
- Task creation: 10 requests per minute
- Task retrieval: 20 requests per minute
- Task updates: 15 requests per minute
- Task deletion: 10 requests per minute
- Task completion toggle: 15 requests per minute

## Running Tests

To run the complete test suite:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=src
```

To run specific test categories:
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/
```

## Health Check

The API provides a health check endpoint:
- `GET /health` - Returns the health status of the API

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success for GET, PUT, PATCH requests
- `201`: Created for POST requests
- `204`: No Content for successful DELETE requests
- `400`: Bad Request for invalid input
- `401`: Unauthorized for invalid/missing JWT
- `404`: Not Found for non-existent resources
- `429`: Too Many Requests for rate-limited requests
- `500`: Internal Server Error for server-side issues

## License

MIT License