# Phase II Frontend (Next.js) Implementation Plan v1.0

## 1. Overview & References
- Linked Specification: Phase II Frontend UI/UX Specification v1.0
- Goals recap: Premium, intuitive, professional frontend UX
- Key Constraints: Agentic workflow, no manual coding, monorepo frontend/ folder

## 2. Technology Stack & Decisions
- Next.js 16+ App Router
- Tailwind CSS + shadcn/ui components
- framer-motion for animations
- next-themes for dark/light mode
- sonner for toasts/notifications
- lucide-react for icons
- PLAN-001: Use shadcn/ui for consistent, high-quality UI components
- PLAN-002: Enable dark mode with system preference support
- PLAN-003: Use TypeScript everywhere

## 3. Frontend Project Structure
- frontend/
  - app/
    - layout.tsx (global layout)
    - login/page.tsx
    - signup/page.tsx
    - tasks/page.tsx (dashboard)
  - components/
    - ui/ (shadcn/ui components)
    - TaskCard.tsx
    - TaskForm.tsx (modal)
    - Navbar.tsx
    - Sidebar.tsx
  - lib/
    - api.ts (fetch wrapper)
    - hooks/
      - useTasks.ts
  - middleware.ts (protected routes)

## 4. High-Level Frontend Architecture
- Root Layout: Navbar + Sidebar (collapsible) + Main content
- Auth Flow: Unauthenticated → login/signup redirect
- Protected Routes: middleware.ts checks auth
- State Management: React Context or Zustand for user/theme
- API Calls: Fetch/axios wrapper with JWT from localStorage/cookies

## 5. Frontend Implementation Plan (Detailed & Prioritized)
- PLAN-004: Global Layout (app/layout.tsx) – Navbar (theme toggle, logout), Sidebar (tasks link), responsive mobile hamburger
- PLAN-005: Auth Pages (login/page.tsx & signup/page.tsx) – Centered forms, validation, loading button, error toasts
- PLAN-006: Tasks Dashboard (app/tasks/page.tsx) – Header (search + add button), task list with view toggle (card/list), empty state CTA
- PLAN-007: Task Card (components/TaskCard.tsx) – Checkbox toggle, inline title edit, desc preview (truncate + expand), edit/delete icons, hover/animation effects
- PLAN-008: Task Form Modal (components/TaskForm.tsx) – Dialog with title input, textarea, validation, submit loading, success toast
- PLAN-009: Global UI Elements – Sonner toasts, loading skeletons, dark mode toggle, ARIA labels, keyboard navigation
- PLAN-010: API Integration (lib/hooks/useTasks.ts) – Custom hook for tasks fetch/mutate, optimistic updates, JWT header attach
- PLAN-011: Responsiveness & Animations – Mobile-first breakpoints, framer-motion fade/slide on task interactions

## 6. Clean Code & Principles
- Type-safe React components with TypeScript
- Reusable shadcn/ui components following design system
- Agentic: All code via Claude Code Frontend Engineer Agent
- Component modularity with clear separation of concerns

## 7. Next Steps & Phase Gates
- After plan approval → /sp.tasks for atomic frontend task breakdown
- Implementation: Use Frontend Engineer Agent for component creation
- Gate: Working frontend with auth flow, task CRUD, responsive design, dark mode
- Gate: All spec requirements (REQ-001 to REQ-005) implemented in frontend