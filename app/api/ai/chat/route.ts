import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { message, agent, threadId, userId } = await request.json();

    if (!message) {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      );
    }

    // Initialize OpenAI (you'll need to add openai package)
    const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

    if (!OPENAI_API_KEY) {
      return NextResponse.json(
        { error: 'OpenAI API key not configured' },
        { status: 500 }
      );
    }

    // Agent system prompts
    const agentPrompts = {
      contract_analyzer: `You are an expert government contract analyst. You analyze RFPs, contracts, and procurement documents. 
                         Provide detailed analysis including: requirements, compliance needs, evaluation criteria, and recommendations.`,
      proposal_writer: `You are an expert proposal writer for government contracts. You help write compelling, compliant proposals.
                       Provide detailed sections, win themes, and compliance matrices.`,
      compliance_checker: `You are a government contracting compliance expert. You check proposals and documents for FAR/DFARS compliance.
                          Identify risks, missing requirements, and provide corrective actions.`,
      opportunity_finder: `You are an expert at finding and analyzing government contracting opportunities on SAM.gov and other sources.
                          Help identify relevant opportunities based on company capabilities.`,
      general: `You are Sturgeon AI, an expert assistant for government contracting. You help with contracts, proposals, compliance, and strategy.`
    };

    const systemPrompt = agentPrompts[agent as keyof typeof agentPrompts] || agentPrompts.general;

    // Call OpenAI API
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: message }
        ],
        temperature: 0.7,
        max_tokens: 2000
      })
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { error: data.error?.message || 'OpenAI API error' },
        { status: response.status }
      );
    }

    const aiMessage = data.choices[0]?.message?.content || 'No response generated';

    return NextResponse.json({
      message: aiMessage,
      agent,
      threadId: threadId || `thread-${Date.now()}`,
      timestamp: new Date().toISOString()
    });

  } catch (error: any) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}
