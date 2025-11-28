import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, password } = body;

    // Use Supabase Auth directly
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
    );

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      return NextResponse.json(
        { detail: error.message },
        { status: 400 }
      );
    }

    return NextResponse.json({ 
      message: 'Registration successful',
      user: data.user 
    });
  } catch (error: any) {
    return NextResponse.json(
      { detail: error.message || 'Registration failed' },
      { status: 500 }
    );
  }
}
