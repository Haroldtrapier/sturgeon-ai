// API Route: /api/grants/[id]/save
// Save a grant for the authenticated user

import { NextApiRequest, NextApiResponse } from 'next';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { id } = req.query;
    const authHeader = req.headers.authorization;

    if (!authHeader) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    // Get user from token
    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error: authError } = await supabase.auth.getUser(token);

    if (authError || !user) {
      return res.status(401).json({ error: 'Invalid token' });
    }

    // Save the grant
    const { error } = await supabase
      .from('saved_grants')
      .insert({
        user_id: user.id,
        grant_id: id,
        notes: req.body.notes || null
      });

    if (error) {
      if (error.code === '23505') { // Unique constraint violation
        return res.status(409).json({ error: 'Grant already saved' });
      }
      throw error;
    }

    res.status(200).json({ success: true });
  } catch (error) {
    console.error('Save grant error:', error);
    res.status(500).json({ error: 'Failed to save grant' });
  }
}
