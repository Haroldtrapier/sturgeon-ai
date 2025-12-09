// AI Agents for Government Contracting
// Uses OpenAI/Anthropic for intelligent contract analysis

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY || '';
const OPENAI_API_KEY = process.env.OPENAI_API_KEY || '';

export interface AgentMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface AgentResponse {
  message: string;
  agent: string;
  timestamp: string;
}

/**
 * Contract Discovery Agent
 * Helps find relevant government contracts based on user requirements
 */
export async function contractDiscoveryAgent(
  userQuery: string,
  context?: any
): Promise<AgentResponse> {
  const systemPrompt = `You are a Contract Discovery Agent specializing in government contracting. 
Your role is to help users find relevant federal contract opportunities from SAM.gov.

When a user asks about contracts:
1. Identify key requirements (NAICS codes, keywords, agencies)
2. Suggest specific search terms for SAM.gov
3. Explain relevant set-aside categories (8(a), SDVOSB, HUBZone, etc.)
4. Provide guidance on qualification requirements

Be concise, actionable, and focus on helping users find opportunities they qualify for.`;

  try {
    const response = await callAIModel([
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userQuery }
    ]);

    return {
      message: response,
      agent: 'Contract Discovery Agent',
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    throw new Error(`Contract Discovery Agent error: ${error}`);
  }
}

/**
 * Proposal Writing Agent
 * Assists with writing government contract proposals
 */
export async function proposalWritingAgent(
  userQuery: string,
  contractDetails?: any
): Promise<AgentResponse> {
  const systemPrompt = `You are a Proposal Writing Agent specialized in federal government contracts.
You help create compelling, compliant proposals that win contracts.

Your expertise includes:
- Technical approach and methodology
- Past performance narratives
- Cost proposals and justifications
- Compliance with FAR requirements
- Executive summaries
- Corporate capability statements

Provide structured, professional content that addresses evaluation criteria.`;

  const contextInfo = contractDetails 
    ? `\n\nContract Context:\n${JSON.stringify(contractDetails, null, 2)}`
    : '';

  try {
    const response = await callAIModel([
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userQuery + contextInfo }
    ]);

    return {
      message: response,
      agent: 'Proposal Writing Agent',
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    throw new Error(`Proposal Writing Agent error: ${error}`);
  }
}

/**
 * Compliance Checker Agent
 * Verifies compliance with FAR, DFARS, and other regulations
 */
export async function complianceCheckerAgent(
  userQuery: string,
  documentContent?: string
): Promise<AgentResponse> {
  const systemPrompt = `You are a Compliance Checker Agent for government contracts.
You verify compliance with:
- Federal Acquisition Regulation (FAR)
- Defense Federal Acquisition Regulation Supplement (DFARS)
- Agency-specific requirements
- Cybersecurity requirements (NIST, CMMC)
- Small business requirements

Identify compliance issues, provide corrections, and cite specific regulations.`;

  const content = documentContent 
    ? `${userQuery}\n\nDocument to review:\n${documentContent}`
    : userQuery;

  try {
    const response = await callAIModel([
      { role: 'system', content: systemPrompt },
      { role: 'user', content }
    ]);

    return {
      message: response,
      agent: 'Compliance Checker Agent',
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    throw new Error(`Compliance Checker Agent error: ${error}`);
  }
}

/**
 * Contract Analysis Agent
 * Analyzes contract requirements and provides insights
 */
export async function contractAnalysisAgent(
  contractData: any
): Promise<AgentResponse> {
  const systemPrompt = `You are a Contract Analysis Agent that reviews government contract opportunities.

Analyze and provide:
1. Key requirements summary
2. Qualification criteria
3. Potential challenges
4. Win probability factors
5. Recommended team structure
6. Cost estimation guidance
7. Timeline considerations

Be analytical and strategic in your assessment.`;

  try {
    const response = await callAIModel([
      { role: 'system', content: systemPrompt },
      { role: 'user', content: `Analyze this contract opportunity:\n\n${JSON.stringify(contractData, null, 2)}` }
    ]);

    return {
      message: response,
      agent: 'Contract Analysis Agent',
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    throw new Error(`Contract Analysis Agent error: ${error}`);
  }
}

/**
 * Teaming Partner Agent
 * Helps find and evaluate potential teaming partners
 */
export async function teamingPartnerAgent(
  userQuery: string,
  requirements?: any
): Promise<AgentResponse> {
  const systemPrompt = `You are a Teaming Partner Agent that helps identify and evaluate potential partners for government contracts.

You provide guidance on:
- Partner selection criteria (capabilities, past performance, certifications)
- Teaming agreement considerations
- Prime vs. subcontractor dynamics
- Small business teaming rules
- Due diligence recommendations
- Complementary capabilities to seek

Help users build winning teams.`;

  const reqInfo = requirements 
    ? `\n\nRequirements:\n${JSON.stringify(requirements, null, 2)}`
    : '';

  try {
    const response = await callAIModel([
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userQuery + reqInfo }
    ]);

    return {
      message: response,
      agent: 'Teaming Partner Agent',
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    throw new Error(`Teaming Partner Agent error: ${error}`);
  }
}

/**
 * Call AI model (Anthropic Claude or OpenAI GPT)
 */
async function callAIModel(messages: AgentMessage[]): Promise<string> {
  // Try Anthropic first
  if (ANTHROPIC_API_KEY) {
    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: 'claude-3-5-sonnet-20241022',
          max_tokens: 4096,
          messages: messages.filter(m => m.role !== 'system'),
          system: messages.find(m => m.role === 'system')?.content
        })
      });

      if (response.ok) {
        const data = await response.json();
        return data.content[0].text;
      }
    } catch (error) {
      console.error('Anthropic API error:', error);
    }
  }

  // Fallback to OpenAI
  if (OPENAI_API_KEY) {
    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${OPENAI_API_KEY}`
        },
        body: JSON.stringify({
          model: 'gpt-4-turbo-preview',
          messages: messages,
          max_tokens: 4096,
          temperature: 0.7
        })
      });

      if (response.ok) {
        const data = await response.json();
        return data.choices[0].message.content;
      }
    } catch (error) {
      console.error('OpenAI API error:', error);
    }
  }

  throw new Error('No AI API key configured. Please set ANTHROPIC_API_KEY or OPENAI_API_KEY');
}

/**
 * Route user message to appropriate agent
 */
export async function routeToAgent(
  message: string,
  context?: any
): Promise<AgentResponse> {
  const lowerMessage = message.toLowerCase();

  // Determine which agent to use based on keywords
  if (lowerMessage.includes('find') || lowerMessage.includes('search') || lowerMessage.includes('discover')) {
    return contractDiscoveryAgent(message, context);
  } else if (lowerMessage.includes('proposal') || lowerMessage.includes('write') || lowerMessage.includes('draft')) {
    return proposalWritingAgent(message, context);
  } else if (lowerMessage.includes('compliance') || lowerMessage.includes('regulation') || lowerMessage.includes('far') || lowerMessage.includes('dfars')) {
    return complianceCheckerAgent(message);
  } else if (lowerMessage.includes('analyze') || lowerMessage.includes('analysis') || lowerMessage.includes('review')) {
    return contractAnalysisAgent(context);
  } else if (lowerMessage.includes('team') || lowerMessage.includes('partner') || lowerMessage.includes('subcontractor')) {
    return teamingPartnerAgent(message);
  }

  // Default to contract discovery
  return contractDiscoveryAgent(message, context);
}
