// API Route: /api/ai/analyze/contract
// Analyze contract text using AI

import { NextApiRequest, NextApiResponse } from 'next';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { text } = req.body;

    if (!text || text.length < 100) {
      return res.status(400).json({ error: 'Contract text is required and must be substantial' });
    }

    const prompt = `Analyze the following government contract and provide:
1. Complexity assessment (low/medium/high)
2. Key requirements (list of 5-10 main requirements)
3. Critical deadlines (with specific dates if available)
4. Risk assessment (potential risks and their severity)
5. Compliance issues (any red flags)
6. Recommendations for the proposal team

Contract text:
${text.substring(0, 8000)}

Respond in JSON format with keys: complexity, keyRequirements, deadlines, risks, complianceIssues, recommendations`;

    const completion = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        {
          role: 'system',
          content: 'You are an expert contract analyst specializing in government contracts. Analyze contracts thoroughly and identify key requirements, risks, and compliance issues.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.3
    });

    const analysis = JSON.parse(completion.choices[0].message.content || '{}');

    res.status(200).json(analysis);
  } catch (error) {
    console.error('Contract analysis error:', error);
    res.status(500).json({ error: 'Failed to analyze contract' });
  }
}
