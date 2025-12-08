import { createClient } from '@supabase/supabase-js';

// Environment variables are required for Supabase client initialization
// Default empty strings allow build to succeed, but runtime will require valid values
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

export const supabaseClient = createClient(supabaseUrl, supabaseAnonKey);
