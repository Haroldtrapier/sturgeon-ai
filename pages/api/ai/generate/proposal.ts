// API Route: /api/ai/generate/proposal
// Generate proposal section content using AI

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
    const { sectionId, context } = req.body;

    if (!sectionId) {
      return res.status(400).json({ error: 'sectionId is required' });
    }

    // Build context-aware prompt
    let prompt = `You are an expert government proposal writer. Generate professional, compelling content for the following proposal section: "${sectionId}".\n\n`;

    if (context.opportunityId) {
      prompt += `This proposal is for opportunity ID: ${context.opportunityId}\n`;
    }

    if (context.previousSections && context.previousSections.length > 0) {
      prompt += `Previous sections context:\n${context.previousSections.join('\n\n')}\n\n`;
    }

    if (context.requirements && context.requirements.length > 0) {
      prompt += `Key requirements to address:\n${context.requirements.map((r, i) => `${i + 1}. ${r}`).join('\n')}\n\n`;
    }

    prompt += `Generate a detailed, professional section that addresses all relevant requirements. Use clear language, provide specific examples where appropriate, and maintain a professional tone suitable for government proposals.`;

    const completion = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        {
          role: 'system',
          content: 'You are an expert government proposal writer with deep knowledge of federal procurement and grant writing.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 2000
    });

    const generatedContent = completion.choices[0].message.content || '';

    res.status(200).json({ content: generatedContent });
  } catch (error) {
    console.error('AI generation error:', error);
    res.status(500).json({ error: 'Failed to generate content' });
  }
}
