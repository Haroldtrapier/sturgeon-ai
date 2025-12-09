// API Route: /api/proposals
// Create or list proposals

import { NextApiRequest, NextApiResponse } from 'next';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const token = authHeader.replace('Bearer ', '');
  const { data: { user }, error: authError } = await supabase.auth.getUser(token);

  if (authError || !user) {
    return res.status(401).json({ error: 'Invalid token' });
  }

  if (req.method === 'GET') {
    // List user's proposals
    const { data: proposals, error } = await supabase
      .from('proposals')
      .select('*, opportunity:opportunities(*)')
      .eq('user_id', user.id)
      .order('updated_at', { ascending: false });

    if (error) {
      return res.status(500).json({ error: 'Failed to fetch proposals' });
    }

    return res.status(200).json({ proposals });
  }

  if (req.method === 'POST') {
    // Create new proposal
    const { title, opportunityId, sections } = req.body;

    if (!title) {
      return res.status(400).json({ error: 'Title is required' });
    }

    const { data: proposal, error: proposalError } = await supabase
      .from('proposals')
      .insert({
        user_id: user.id,
        title,
        opportunity_id: opportunityId || null,
        status: 'draft'
      })
      .select()
      .single();

    if (proposalError) {
      return res.status(500).json({ error: 'Failed to create proposal' });
    }

    // Create default sections if provided
    if (sections && sections.length > 0) {
      const sectionData = sections.map((s: any, idx: number) => ({
        proposal_id: proposal.id,
        section_id: s.id || `section_${idx}`,
        title: s.title,
        content: s.content || '',
        required: s.required || false,
        order_index: idx
      }));

      await supabase.from('proposal_sections').insert(sectionData);
    }

    return res.status(201).json(proposal);
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
