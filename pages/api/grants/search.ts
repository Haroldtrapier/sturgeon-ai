// API Route: /api/grants/search
// Search grants from multiple sources

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
    const { keyword, agency, category, minAmount, maxAmount, deadline } = req.body;

    let query = supabase
      .from('grants')
      .select('*')
      .order('deadline', { ascending: true });

    // Apply filters
    if (keyword) {
      query = query.or(`title.ilike.%${keyword}%,description.ilike.%${keyword}%`);
    }

    if (agency) {
      query = query.eq('agency', agency);
    }

    if (category) {
      query = query.eq('category', category);
    }

    if (deadline) {
      query = query.lte('deadline', deadline);
    }

    const { data: grants, error } = await query;

    if (error) throw error;

    // Filter by amount (stored as string, needs parsing)
    let filteredGrants = grants || [];

    if (minAmount || maxAmount) {
      filteredGrants = filteredGrants.filter(grant => {
        const amount = parseFloat(grant.amount?.replace(/[^0-9.-]+/g, '') || '0');
        if (minAmount && amount < parseFloat(minAmount)) return false;
        if (maxAmount && amount > parseFloat(maxAmount)) return false;
        return true;
      });
    }

    res.status(200).json({ grants: filteredGrants });
  } catch (error) {
    console.error('Grants search error:', error);
    res.status(500).json({ error: 'Failed to search grants' });
  }
}
