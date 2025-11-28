// Supabase client - no Prisma needed since we're using Supabase
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

// For server-side use with service role key
export const supabase = createClient(supabaseUrl, supabaseKey);

// Export a mock prisma object for compatibility if needed
export const prisma = null;
