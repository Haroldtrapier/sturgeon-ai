import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
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
    // Sign out from Supabase with global scope to clear all sessions
    const { error } = await supabase.auth.signOut({ scope: 'global' });

    if (error) {
      console.error('Supabase sign out error:', error);
      // Continue with logout process even if Supabase signout fails
      // to ensure user can still clear local auth state
    }

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
