import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { verifyToken, extractTokenFromCookies } from './lib/auth';

// Routes that require authentication
const protectedRoutes = ['/dashboard', '/analytics', '/opportunities', '/proposals', '/payments'];

// Public routes that don't require authentication
const publicRoutes = ['/login', '/signup', '/forgot-password', '/'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check if route needs protection
  const isProtectedRoute = protectedRoutes.some(route => pathname.startsWith(route));
  const isPublicRoute = publicRoutes.some(route => pathname === route);

  // Skip middleware for API routes, static files, and public routes
  if (pathname.startsWith('/api') || pathname.startsWith('/_next') || pathname.startsWith('/static') || isPublicRoute) {
    return NextResponse.next();
  }

  // For protected routes, verify authentication
  if (isProtectedRoute) {
    // Try to get token from cookies first
    const cookieToken = extractTokenFromCookies(request.headers.get('cookie'));

    // Try Authorization header as fallback
    const authHeader = request.headers.get('authorization');
    const headerToken = authHeader?.startsWith('Bearer ') ? authHeader.substring(7) : null;

    const token = cookieToken || headerToken;

    // No token found, redirect to login
    if (!token) {
      const url = new URL('/login', request.url);
      url.searchParams.set('redirect', pathname);
      return NextResponse.redirect(url);
    }

    // Verify token
    const user = verifyToken(token);

    if (!user) {
      // Invalid token, redirect to login
      const url = new URL('/login', request.url);
      url.searchParams.set('redirect', pathname);
      return NextResponse.redirect(url);
    }

    // Token is valid, allow access
    return NextResponse.next();
  }

  // For all other routes, allow access
  return NextResponse.next();
}

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
