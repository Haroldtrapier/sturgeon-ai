import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { comparePassword } from '@/lib/auth';
import { generateToken, generateRefreshToken } from '@/lib/auth';
import { setAuthCookie, createErrorResponse, createSuccessResponse } from '@/lib/api';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { email, password } = body;

    // Validate input
    if (!email || !password) {
      return createErrorResponse('Email and password are required', 400);
    }

    // Find user in database
    const { data: user, error } = await supabase
      .from('users')
      .select('*')
      .eq('email', email.toLowerCase())
      .single();

    if (error || !user) {
      return createErrorResponse('Invalid email or password', 401);
    }

    // Verify password
    const isValidPassword = await comparePassword(password, user.password_hash);

    if (!isValidPassword) {
      return createErrorResponse('Invalid email or password', 401);
    }

    // Generate tokens
    const userPayload = {
      id: user.id,
      email: user.email,
      name: user.name,
    };

    const token = generateToken(userPayload);
    const refreshToken = generateRefreshToken(userPayload);

    // Create response
    const response = NextResponse.json(
      createSuccessResponse({
        token,
        refreshToken,
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
        },
      }, 'Login successful')
    );

    // Set secure cookies
    setAuthCookie(response, token, refreshToken);

    return response;
  } catch (error: any) {
    console.error('Login error:', error);
    return createErrorResponse('An error occurred during login', 500);
  }
}
