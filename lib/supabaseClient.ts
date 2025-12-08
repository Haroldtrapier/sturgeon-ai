import { supabase } from '@/lib/supabase';

/**
 * Handle user logout
 * Signs out from Supabase and redirects to login page
 */
export async function handleLogout() {
  try {
    const { error } = await supabase.auth.signOut();
    if (error) {
      console.error('Logout error:', error);
      // Still redirect to login even if there's an error
      // The user's intent is to log out, so we should honor that
    }
    window.location.href = '/login';
  } catch (error) {
    console.error('Unexpected logout error:', error);
    window.location.href = '/login';
  }
}

// Re-export supabase client for convenience
export { supabase };
