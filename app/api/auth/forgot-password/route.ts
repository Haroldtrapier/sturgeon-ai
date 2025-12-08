import { NextResponse } from 'next/server';
import { supabaseClient } from '@/lib/supabaseClient';

// Enable CORS
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export async function OPTIONS() {
  return NextResponse.json({}, { headers: corsHeaders });
}

export async function POST(req: Request) {
  try {
    const { email } = await req.json();

    if (!email) {
      return NextResponse.json({ error: 'Email is required.' }, { status: 400, headers: corsHeaders });
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return NextResponse.json({ error: 'Invalid email format.' }, { status: 400, headers: corsHeaders });
    }

    const redirectUrl =
      process.env.NEXT_PUBLIC_RESET_REDIRECT_URL ??
      `${process.env.NEXT_PUBLIC_BASE_URL ?? ''}/reset-password`;

    const { error } = await supabaseClient.auth.resetPasswordForEmail(email, {
      redirectTo: redirectUrl,
    });

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 400, headers: corsHeaders });
    }

    return NextResponse.json(
      { message: 'Password reset email sent. Please check your inbox.' },
      { status: 200, headers: corsHeaders }
    );
  } catch (err) {
    console.error('Forgot-password error', err);
    return NextResponse.json({ error: 'Unexpected error during password reset.' }, { status: 500, headers: corsHeaders });
  }
}
