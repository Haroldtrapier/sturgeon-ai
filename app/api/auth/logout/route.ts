import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { clearAuthCookies, createSuccessResponse } from '@/lib/api';

// Enable CORS
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export async function OPTIONS() {
  return NextResponse.json({}, { headers: corsHeaders });
}

export async function POST(request: Request) {
  try {
    // Check environment variables
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

    if (!supabaseUrl || !supabaseAnonKey) {
      console.error('Missing Supabase environment variables');
      return NextResponse.json(
        { error: 'Server configuration error. Please contact support.' },
        { status: 500, headers: corsHeaders }
      );
    }

    // Create Supabase client
    const supabase = createClient(supabaseUrl, supabaseAnonKey);

    // Sign out from Supabase
    await supabase.auth.signOut();

    // Create response
    const response = NextResponse.json(
      createSuccessResponse({ message: 'Logged out successfully' }, 'Logout successful'),
      { headers: corsHeaders }
    );

    // Clear auth cookies
    clearAuthCookies(response);

    return response;
  } catch (error: any) {
    console.error('Logout error:', error);
    return NextResponse.json(
      { error: error.message || 'An unexpected error occurred during logout' },
      { status: 500, headers: corsHeaders }
    );
  }
}
