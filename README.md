# Todo Full-Stack Web Application - Phase II

This is the frontend implementation of a multi-user full-stack todo application with premium frontend UX using Next.js, Tailwind CSS, shadcn/ui, and other modern technologies. The application provides user authentication, task management with CRUD operations, and a responsive, accessible UI.

## Features

- User authentication (signup/login)
- Task CRUD operations (Create, Read, Update, Delete)
- Responsive design for mobile, tablet, and desktop
- Dark/light mode support
- Animations and transitions
- Search and sort functionality
- Error handling and edge cases

## Tech Stack

- Next.js 16+ with App Router
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Framer Motion for animations
- Sonner for toast notifications

## Getting Started

First, install the dependencies:

```bash
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Environment Variables

Create a `.env.local` file in the `frontend` directory with the following variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

## Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint to check for code issues

## Project Structure

- `frontend/` - Next.js frontend application
- `backend/` - FastAPI backend application (to be implemented)
- `specs/` - Project specifications
- `history/` - Project history and documentation