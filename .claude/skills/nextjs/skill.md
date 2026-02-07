# Next.js Development Skill

## Purpose
This skill provides expert guidance and implementation assistance for Next.js applications following best practices and modern development patterns.

## Capabilities
- Create and configure Next.js applications
- Implement page and layout structures using App Router
- Build API routes and server-side rendering solutions
- Handle authentication and authorization flows
- Optimize performance with caching and static generation
- Implement responsive UI with Tailwind CSS
- Manage state with React Context and client-side stores
- Integrate with backend services and databases
- Configure deployment settings for various platforms

## Best Practices to Follow
- Use the App Router (`app/` directory) for new projects
- Implement proper TypeScript typing throughout
- Follow accessibility guidelines (WCAG)
- Use server components when possible for better performance
- Implement proper error boundaries and loading states
- Apply responsive design principles
- Use environment variables for configuration
- Implement proper SEO meta tags and structured data

## Common Patterns
- Page and layout composition with React Server Components
- Client Components for interactivity using `"use client"`
- Route handlers for API endpoints in `app/api/`
- Loading and error UI states
- Form handling with React Hook Form or native forms
- Image optimization with `next/image`
- Link handling with `next/link`

## File Structure Convention
```
app/
├── layout.tsx          # Root layout
├── page.tsx           # Home page
├── components/        # Shared components
├── lib/              # Utility functions
├── styles/           # Global styles
└── api/              # API routes
```

## Technical Requirements
- Always use TypeScript over JavaScript
- Implement proper error handling
- Use Zod for schema validation
- Follow RESTful API design for route handlers
- Apply proper HTTP status codes
- Use semantic HTML elements
- Implement proper meta tags for SEO