// API Route: /api/grants/sync/grants-gov
// Sync grants from Grants.gov API

import { NextApiRequest, NextApiResponse } from 'next';
import { createClient } from '@supabase/supabase-js';
import axios from 'axios';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

const GRANTS_GOV_API = 'https://www.grants.gov/grantsws/rest/opportunities/search';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const apiKey = process.env.GRANTS_GOV_API_KEY;

    if (!apiKey) {
      return res.status(500).json({ error: 'Grants.gov API key not configured' });
    }

    // Fetch from Grants.gov
    const response = await axios.get(GRANTS_GOV_API, {
      headers: { 'Authorization': `Bearer ${apiKey}` },
      params: {
        rows: 100,
        startRecordNum: 0,
        oppStatuses: 'forecasted|posted'
      }
    });

    const opportunities = response.data.oppHits || [];
    let synced = 0;
    let failed = 0;

    // Insert/update grants
    for (const opp of opportunities) {
      try {
        const grantData = {
          external_id: opp.id,
          title: opp.title,
          agency: opp.agency Code,
          amount: opp.awardCeiling || 'Not specified',
          deadline: opp.closeDate,
          category: opp.category || 'general',
          description: opp.description,
          eligibility: opp.eligibility || [],
          source: 'grants.gov',
          metadata: {
            cfda: opp.cfdaList,
            fundingInstruments: opp.fundingInstruments,
            costSharing: opp.costSharing
          }
        };

        const { error } = await supabase
          .from('grants')
          .upsert(grantData, { onConflict: 'external_id' });

        if (error) {
          console.error('Failed to sync grant:', opp.id, error);
          failed++;
        } else {
          synced++;
        }
      } catch (err) {
        console.error('Error processing grant:', err);
        failed++;
      }
    }

    res.status(200).json({ synced, failed, total: opportunities.length });
  } catch (error) {
    console.error('Grants sync error:', error);
    res.status(500).json({ error: 'Failed to sync grants' });
  }
}
