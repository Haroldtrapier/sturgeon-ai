import { supabase } from '@/lib/supabase';

/**
 * Handle user logout
 * Signs out from Supabase and redirects to login page
 */
export async function handleLogout() {
  await supabase.auth.signOut();
  window.location.href = '/login';
}

// Re-export supabase client for convenience
export { supabase };
