// Compliance API Service - FAR, DFARS, FISMA, CMMC checks

export interface ComplianceCheck {
  id: string;
  category: string;
  requirement: string;
  status: 'passed' | 'failed' | 'warning' | 'pending';
  details: string;
  reference: string;
}

export interface ComplianceReport {
  overallStatus: 'compliant' | 'non-compliant' | 'needs-review';
  score: number;
  checks: ComplianceCheck[];
  recommendations: string[];
}

export type RegulationType = 'FAR' | 'DFARS' | 'FISMA' | 'CMMC' | 'ALL';

class ComplianceAPIService {
  private baseUrl = '/api/compliance';

  async runComplianceCheck(
    documentId: string,
    regulationType: RegulationType
  ): Promise<ComplianceReport> {
    const response = await fetch(`${this.baseUrl}/check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ documentId, regulationType })
    });

    if (!response.ok) {
      throw new Error('Compliance check failed');
    }

    return response.json();
  }

  async getComplianceHistory(documentId: string): Promise<ComplianceReport[]> {
    const response = await fetch(`${this.baseUrl}/history/${documentId}`);

    if (!response.ok) {
      throw new Error('Failed to fetch compliance history');
    }

    const data = await response.json();
    return data.reports;
  }

  async getFARRequirements(): Promise<ComplianceCheck[]> {
    const response = await fetch(`${this.baseUrl}/requirements/FAR`);

    if (!response.ok) {
      throw new Error('Failed to fetch FAR requirements');
    }

    const data = await response.json();
    return data.requirements;
  }

  async getDFARSRequirements(): Promise<ComplianceCheck[]> {
    const response = await fetch(`${this.baseUrl}/requirements/DFARS`);

    if (!response.ok) {
      throw new Error('Failed to fetch DFARS requirements');
    }

    const data = await response.json();
    return data.requirements;
  }
}

export const complianceAPI = new ComplianceAPIService();
