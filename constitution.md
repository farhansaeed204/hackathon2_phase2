# Project Constitution

## Purpose
This document defines the guiding principles and architectural decisions for the Hackathon II Phase II project.

## Core Values
- Clean, maintainable code with proper separation of concerns
- Secure authentication and authorization using JWT tokens
- Efficient database operations with Neon Postgres and SQLModel
- Responsive UI with Next.js App Router and shadcn/ui components
- Proper error handling and validation throughout the application

## Technical Principles
- Use async/await for all database operations
- Implement proper JWT token validation and user ID verification
- Follow RESTful API design patterns
- Maintain consistent error responses across the application
- Use environment variables for configuration
- Implement proper logging for debugging and monitoring

## Architecture
- Frontend: Next.js 14 with App Router, Tailwind CSS, and shadcn/ui components
- Backend: FastAPI with SQLModel and Neon Postgres
- Authentication: JWT-based with BETTER_AUTH_SECRET
- Database: Neon Postgres with async connections
- Deployment: Vercel for frontend, Render for backend

## Quality Standards
- All code must include proper type hints
- All functions must have docstrings
- Error handling must be comprehensive
- API responses must follow consistent format
- Security best practices must be followed