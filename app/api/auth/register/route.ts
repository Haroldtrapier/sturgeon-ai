import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { hashPassword, generateToken, generateRefreshToken } from '@/lib/auth';
import { setAuthCookie, createErrorResponse, createSuccessResponse, validateRequiredFields } from '@/lib/api';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { email, password, name } = body;

    // Validate required fields
    const validation = validateRequiredFields(body, ['email', 'password', 'name']);
    if (!validation.valid) {
      return createErrorResponse(`Missing required fields: ${validation.missing?.join(', ')}`, 400);
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return createErrorResponse('Invalid email format', 400);
    }

    // Validate password strength (min 8 characters)
    if (password.length < 8) {
      return createErrorResponse('Password must be at least 8 characters long', 400);
    }

    // Check if user already exists
    const { data: existingUser } = await supabase
      .from('users')
      .select('id')
      .eq('email', email.toLowerCase())
      .single();

    if (existingUser) {
      return createErrorResponse('User with this email already exists', 409);
    }

    // Hash password
    const passwordHash = await hashPassword(password);

    // Create user
    const { data: newUser, error } = await supabase
      .from('users')
      .insert({
        email: email.toLowerCase(),
        name,
        password_hash: passwordHash,
        created_at: new Date().toISOString(),
      })
      .select()
      .single();

    if (error) {
      console.error('Database error:', error);
      return createErrorResponse('Failed to create user', 500);
    }

    // Generate tokens
    const userPayload = {
      id: newUser.id,
      email: newUser.email,
      name: newUser.name,
    };

    const token = generateToken(userPayload);
    const refreshToken = generateRefreshToken(userPayload);

    // Create response
    const response = NextResponse.json(
      createSuccessResponse({
        token,
        refreshToken,
        user: {
          id: newUser.id,
          email: newUser.email,
          name: newUser.name,
        },
      }, 'Registration successful')
    );

    // Set secure cookies
    setAuthCookie(response, token, refreshToken);

    return response;
  } catch (error: any) {
    console.error('Registration error:', error);
    return createErrorResponse('An error occurred during registration', 500);
  }
}
