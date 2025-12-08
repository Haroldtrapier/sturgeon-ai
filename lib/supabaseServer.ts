import { cookies } from 'next/headers';
import { createServerClient, type CookieOptions } from '@supabase/ssr';

export const createServerSupabaseClient = () => {
  const cookieStore = cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        set(name: string, value: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value, ...options });
          } catch (error) {
            // Cookie setting can fail in certain contexts (e.g., after response headers are sent)
            // This is expected behavior in some server-side scenarios
          }
        },
        remove(name: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value: '', ...options, maxAge: 0 });
          } catch (error) {
            // Cookie removal can fail in certain contexts
            // This is expected behavior in some server-side scenarios
          }
        },
      },
    }
  );
};
