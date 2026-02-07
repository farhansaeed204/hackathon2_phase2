import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Check for authentication token
  const token = request.cookies.get('auth-token') || request.headers.get('authorization');

  // Define protected routes
  const protectedPaths = ['/tasks', '/settings'];
  const currentPath = request.nextUrl.pathname;

  // If accessing a protected route without authentication
  if (protectedPaths.some(path => currentPath.startsWith(path)) && !token) {
    // Redirect to login page
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Continue with the request
  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};