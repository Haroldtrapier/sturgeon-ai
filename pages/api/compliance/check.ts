// API Route: /api/compliance/check
// Run compliance check on document or proposal

import { NextApiRequest, NextApiResponse } from 'next';
import { createClient } from '@supabase/supabase-js';
import OpenAI from 'openai';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Compliance requirements database
const COMPLIANCE_RULES = {
  FAR: [
    { id: 'far_1', category: 'Contract Formation', requirement: 'Proper competition procedures', reference: 'FAR Part 6' },
    { id: 'far_2', category: 'Pricing', requirement: 'Cost and pricing data requirements', reference: 'FAR 15.403' },
    { id: 'far_3', category: 'Contract Clauses', requirement: 'Required contract clauses included', reference: 'FAR Part 52' }
  ],
  DFARS: [
    { id: 'dfars_1', category: 'Security', requirement: 'Cybersecurity requirements', reference: 'DFARS 252.204-7012' },
    { id: 'dfars_2', category: 'Supply Chain', requirement: 'Supply chain risk management', reference: 'DFARS 252.204-7015' }
  ],
  FISMA: [
    { id: 'fisma_1', category: 'Information Security', requirement: 'Security controls implementation', reference: 'NIST SP 800-53' }
  ],
  CMMC: [
    { id: 'cmmc_1', category: 'Access Control', requirement: 'Multi-factor authentication', reference: 'CMMC Level 2' },
    { id: 'cmmc_2', category: 'Incident Response', requirement: 'Incident response plan', reference: 'CMMC Level 2' }
  ]
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { documentId, proposalId, regulationType } = req.body;

    if (!documentId && !proposalId) {
      return res.status(400).json({ error: 'documentId or proposalId required' });
    }

    // Get document/proposal content
    let content = '';
    if (documentId) {
      const { data: doc } = await supabase
        .from('documents')
        .select('parsed_content')
        .eq('id', documentId)
        .single();
      content = doc?.parsed_content || '';
    } else if (proposalId) {
      const { data: sections } = await supabase
        .from('proposal_sections')
        .select('content')
        .eq('proposal_id', proposalId);
      content = sections?.map(s => s.content).join('\n\n') || '';
    }

    if (!content) {
      return res.status(400).json({ error: 'No content found to check' });
    }

    // Get applicable rules
    const rules = regulationType === 'ALL' 
      ? [...COMPLIANCE_RULES.FAR, ...COMPLIANCE_RULES.DFARS, ...COMPLIANCE_RULES.FISMA, ...COMPLIANCE_RULES.CMMC]
      : COMPLIANCE_RULES[regulationType as keyof typeof COMPLIANCE_RULES] || [];

    // AI-powered compliance checking
    const prompt = `Analyze the following document for compliance with these requirements:

${rules.map((r, i) => `${i + 1}. ${r.requirement} (${r.reference})`).join('\n')}

Document content:
${content.substring(0, 6000)}

For each requirement, determine: passed, failed, warning, or pending.
Provide overall compliance score (0-100), status (compliant/non-compliant/needs-review), and recommendations.

Respond in JSON format with: { score, overallStatus, checks: [{id, status, details}], recommendations: [] }`;

    const completion = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        { role: 'system', content: 'You are a compliance expert specializing in FAR, DFARS, FISMA, and CMMC regulations.' },
        { role: 'user', content: prompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.2
    });

    const analysis = JSON.parse(completion.choices[0].message.content || '{}');

    // Enhance checks with requirement details
    const enhancedChecks = analysis.checks.map((check: any) => {
      const rule = rules.find(r => r.id === check.id) || rules[0];
      return {
        ...check,
        category: rule.category,
        requirement: rule.requirement,
        reference: rule.reference
      };
    });

    const report = {
      overallStatus: analysis.overallStatus,
      score: analysis.score,
      checks: enhancedChecks,
      recommendations: analysis.recommendations || []
    };

    // Save report
    const { data: savedReport } = await supabase
      .from('compliance_reports')
      .insert({
        document_id: documentId || null,
        proposal_id: proposalId || null,
        regulation_type: regulationType,
        overall_status: report.overallStatus,
        score: report.score,
        checks: report.checks,
        recommendations: report.recommendations
      })
      .select()
      .single();

    res.status(200).json(report);
  } catch (error) {
    console.error('Compliance check error:', error);
    res.status(500).json({ error: 'Failed to run compliance check' });
  }
}
