// Grants API Service - Integration with grants.gov and usaspending.gov

export interface Grant {
  id: string;
  title: string;
  agency: string;
  amount: string;
  deadline: string;
  category: string;
  description: string;
  eligibility: string[];
  matchScore?: number;
}

export interface GrantFilters {
  keyword?: string;
  agency?: string;
  category?: string;
  minAmount?: number;
  maxAmount?: number;
  deadline?: string;
}

class GrantsAPIService {
  private baseUrl = '/api/grants';

  async searchGrants(filters: GrantFilters): Promise<Grant[]> {
    const response = await fetch(`${this.baseUrl}/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(filters)
    });

    if (!response.ok) {
      throw new Error('Failed to search grants');
    }

    const data = await response.json();
    return data.grants;
  }

  async getGrantDetails(grantId: string): Promise<Grant> {
    const response = await fetch(`${this.baseUrl}/${grantId}`);

    if (!response.ok) {
      throw new Error('Failed to fetch grant details');
    }

    return response.json();
  }

  async saveGrant(grantId: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/${grantId}/save`, {
      method: 'POST'
    });

    if (!response.ok) {
      throw new Error('Failed to save grant');
    }
  }

  async getSavedGrants(): Promise<Grant[]> {
    const response = await fetch(`${this.baseUrl}/saved`);

    if (!response.ok) {
      throw new Error('Failed to fetch saved grants');
    }

    const data = await response.json();
    return data.grants;
  }

  async syncFromGrantsGov(): Promise<{ synced: number; failed: number }> {
    const response = await fetch(`${this.baseUrl}/sync/grants-gov`, {
      method: 'POST'
    });

    if (!response.ok) {
      throw new Error('Failed to sync from grants.gov');
    }

    return response.json();
  }

  async syncFromUSASpending(): Promise<{ synced: number; failed: number }> {
    const response = await fetch(`${this.baseUrl}/sync/usaspending`, {
      method: 'POST'
    });

    if (!response.ok) {
      throw new Error('Failed to sync from USASpending.gov');
    }

    return response.json();
  }
}

export const grantsAPI = new GrantsAPIService();
