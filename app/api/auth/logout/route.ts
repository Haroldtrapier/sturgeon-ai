import { NextResponse } from 'next/server';
import { clearAuthCookies, createSuccessResponse } from '@/lib/api';

export async function POST(request: Request) {
  const response = NextResponse.json(
    createSuccessResponse({ message: 'Logged out successfully' }, 'Logout successful')
  );

  // Clear auth cookies
  clearAuthCookies(response);

  return response;
}
