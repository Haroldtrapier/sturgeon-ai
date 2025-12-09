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

    // Get API keys
    const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
    const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

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

    let aiMessage = '';
    let provider = '';

    // Try Claude first (Primary)
    if (ANTHROPIC_API_KEY) {
      try {
        console.log('Attempting Claude API...');
        const claudeResponse = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01'
          },
          body: JSON.stringify({
            model: 'claude-3-5-sonnet-20241022',
            max_tokens: 4096,
            system: systemPrompt,
            messages: [
              { role: 'user', content: message }
            ]
          })
        });

        if (claudeResponse.ok) {
          const claudeData = await claudeResponse.json();
          aiMessage = claudeData.content[0]?.text || 'No response generated';
          provider = 'Claude (Anthropic)';
          console.log('Claude succeeded');
        } else {
          throw new Error(`Claude API error: ${claudeResponse.status}`);
        }
      } catch (claudeError: any) {
        console.log('Claude failed, falling back to OpenAI:', claudeError.message);

        // Fallback to OpenAI (Secondary)
        if (OPENAI_API_KEY) {
          const openaiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${OPENAI_API_KEY}`
            },
            body: JSON.stringify({
              model: 'gpt-4o',
              messages: [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: message }
              ],
              temperature: 0.7,
              max_tokens: 2000
            })
          });

          const openaiData = await openaiResponse.json();

          if (!openaiResponse.ok) {
            throw new Error(openaiData.error?.message || 'OpenAI API error');
          }

          aiMessage = openaiData.choices[0]?.message?.content || 'No response generated';
          provider = 'ChatGPT (OpenAI Fallback)';
        } else {
          throw new Error('Both Claude and OpenAI API keys are missing');
        }
      }
    } else if (OPENAI_API_KEY) {
      // No Claude key, use OpenAI directly
      console.log('Claude key not found, using OpenAI...');
      const openaiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${OPENAI_API_KEY}`
        },
        body: JSON.stringify({
          model: 'gpt-4o',
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: message }
          ],
          temperature: 0.7,
          max_tokens: 2000
        })
      });

      const openaiData = await openaiResponse.json();

      if (!openaiResponse.ok) {
        throw new Error(openaiData.error?.message || 'OpenAI API error');
      }

      aiMessage = openaiData.choices[0]?.message?.content || 'No response generated';
      provider = 'ChatGPT (OpenAI)';
    } else {
      throw new Error('No AI API keys configured. Please add ANTHROPIC_API_KEY or OPENAI_API_KEY to your environment variables.');
    }

    return NextResponse.json({
      message: aiMessage,
      provider,
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
