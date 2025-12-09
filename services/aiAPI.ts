// AI API Service - Proposal generation, contract analysis, chat

export interface AIGenerationRequest {
  sectionId: string;
  context: {
    opportunityId?: string;
    previousSections?: string[];
    requirements?: string[];
  };
}

export interface ContractAnalysis {
  complexity: 'low' | 'medium' | 'high';
  keyRequirements: string[];
  deadlines: { item: string; date: string }[];
  risks: { level: string; description: string }[];
  recommendations: string[];
  complianceIssues: string[];
}

class AIAPIService {
  private baseUrl = '/api/ai';

  async generateProposalSection(request: AIGenerationRequest): Promise<string> {
    const response = await fetch(`${this.baseUrl}/generate/proposal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error('AI generation failed');
    }

    const data = await response.json();
    return data.content;
  }

  async analyzeContract(contractText: string): Promise<ContractAnalysis> {
    const response = await fetch(`${this.baseUrl}/analyze/contract`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: contractText })
    });

    if (!response.ok) {
      throw new Error('Contract analysis failed');
    }

    return response.json();
  }

  async chat(message: string, history: any[]): Promise<string> {
    const response = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history })
    });

    if (!response.ok) {
      throw new Error('AI chat failed');
    }

    const data = await response.json();
    return data.response;
  }

  async extractRequirements(documentText: string): Promise<string[]> {
    const response = await fetch(`${this.baseUrl}/extract/requirements`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: documentText })
    });

    if (!response.ok) {
      throw new Error('Requirements extraction failed');
    }

    const data = await response.json();
    return data.requirements;
  }
}

export const aiAPI = new AIAPIService();
