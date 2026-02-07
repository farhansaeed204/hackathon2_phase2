# Quickstart Guide

## Prerequisites
- Python 3.11+
- pip package manager
- Neon Postgres account and database URL
- Better Auth secret key

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn src.main:app --reload
   ```

## Environment Variables
- `NEON_DB_URL`: Your Neon Postgres database connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT verification
- `BETTER_AUTH_URL`: Better Auth instance URL

## API Endpoints
- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Testing
Run the test suite:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=src
```