import { useState, useEffect, useCallback } from 'react';

interface Opportunity {
  id: string;
  title: string;
  agency: string;
  deadline: string;
  // ... other fields
}

interface UseOpportunitiesResult {
  opportunities: Opportunity[];
  isLoading: boolean;
  error: Error | null;
  fetchOpportunities: (filters?: any) => Promise<void>;
  saveOpportunity: (id: string) => Promise<void>;
  unsaveOpportunity: (id: string) => Promise<void>;
}

export const useOpportunities = (): UseOpportunitiesResult => {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchOpportunities = useCallback(async (filters = {}) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/opportunities', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filters)
      });
      if (!response.ok) throw new Error('Failed to fetch opportunities');
      const data = await response.json();
      setOpportunities(data.opportunities || []);
    } catch (err) {
      setError(err as Error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const saveOpportunity = useCallback(async (id: string) => {
    try {
      await fetch(`/api/opportunities/${id}/save`, { method: 'POST' });
      // Update local state or refetch
    } catch (err) {
      console.error('Failed to save opportunity:', err);
    }
  }, []);

  const unsaveOpportunity = useCallback(async (id: string) => {
    try {
      await fetch(`/api/opportunities/${id}/unsave`, { method: 'POST' });
      // Update local state or refetch
    } catch (err) {
      console.error('Failed to unsave opportunity:', err);
    }
  }, []);

  useEffect(() => {
    fetchOpportunities();
  }, [fetchOpportunities]);

  return {
    opportunities,
    isLoading,
    error,
    fetchOpportunities,
    saveOpportunity,
    unsaveOpportunity
  };
};
