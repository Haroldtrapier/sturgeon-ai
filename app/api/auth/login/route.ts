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

    // Sign in user
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      console.error('Supabase sign in error:', error);
      return NextResponse.json(
        { error: error.message },
        { status: 401, headers: corsHeaders }
      );
    }

    // Return success with session
    return NextResponse.json(
      { 
        success: true,
        message: 'Login successful!',
        user: {
          id: data.user?.id,
          email: data.user?.email,
        },
        session: {
          access_token: data.session?.access_token,
          refresh_token: data.session?.refresh_token,
        }
      },
      { status: 200, headers: corsHeaders }
    );
  } catch (error: any) {
    console.error('Login error:', error);
    return NextResponse.json(
      { error: error.message || 'An unexpected error occurred' },
      { status: 500, headers: corsHeaders }
    );
  }
}
