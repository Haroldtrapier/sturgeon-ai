import { NextResponse } from 'next/server';
import { supabaseClient } from '@/lib/supabaseClient';

export async function POST() {
  try {
    const { error } = await supabaseClient.auth.signOut();
    if (error) {
      return NextResponse.json({ error: error.message }, { status: 400 });
    }
    return NextResponse.json({ message: 'Logged out' }, { status: 200 });
  } catch (err) {
    console.error('Logout error', err instanceof Error ? err.message : 'Unknown error');
    return NextResponse.json({ error: 'Unexpected error during logout.' }, { status: 500 });
  }
}
