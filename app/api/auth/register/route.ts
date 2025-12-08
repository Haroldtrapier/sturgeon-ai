import { NextRequest, NextResponse } from 'next/server';
import { supabaseClient as supabase } from '@/lib/supabaseClient';

// Enable CORS
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export async function OPTIONS() {
  return NextResponse.json({}, { headers: corsHeaders });
}

export async function POST(request: NextRequest) {
  try {
    // Parse request body
    const body = await request.json();
    const { email, password } = body;

    // Validate input
    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password are required' },
        { status: 400, headers: corsHeaders }
      );
    }

    // Sign up user
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      console.error('Supabase sign up error:', error);
      return NextResponse.json(
        { error: error.message },
        { status: 400, headers: corsHeaders }
      );
    }

    // Return success
    return NextResponse.json(
      { 
        success: true,
        message: 'Registration successful! Please check your email to confirm your account.',
        user: {
          id: data.user?.id,
          email: data.user?.email,
        }
      },
      { status: 201, headers: corsHeaders }
    );
  } catch (error: any) {
    console.error('Registration error:', error);
    return NextResponse.json(
      { error: error.message || 'An unexpected error occurred' },
      { status: 500, headers: corsHeaders }
    );
  }
}
