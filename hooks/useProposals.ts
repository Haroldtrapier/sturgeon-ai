import { useState, useCallback } from 'react';

interface Proposal {
  id: string;
  title: string;
  status: 'draft' | 'in-progress' | 'submitted';
  // ... other fields
}

interface UseProposalsResult {
  proposals: Proposal[];
  isLoading: boolean;
  error: Error | null;
  createProposal: (data: Partial<Proposal>) => Promise<Proposal>;
  updateProposal: (id: string, data: Partial<Proposal>) => Promise<void>;
  deleteProposal: (id: string) => Promise<void>;
  submitProposal: (id: string) => Promise<void>;
}

export const useProposals = (): UseProposalsResult => {
  const [proposals, setProposals] = useState<Proposal[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const createProposal = useCallback(async (data: Partial<Proposal>) => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/proposals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!response.ok) throw new Error('Failed to create proposal');
      const newProposal = await response.json();
      setProposals(prev => [...prev, newProposal]);
      return newProposal;
    } catch (err) {
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const updateProposal = useCallback(async (id: string, data: Partial<Proposal>) => {
    try {
      const response = await fetch(`/api/proposals/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!response.ok) throw new Error('Failed to update proposal');
      const updated = await response.json();
      setProposals(prev => prev.map(p => p.id === id ? updated : p));
    } catch (err) {
      setError(err as Error);
    }
  }, []);

  const deleteProposal = useCallback(async (id: string) => {
    try {
      await fetch(`/api/proposals/${id}`, { method: 'DELETE' });
      setProposals(prev => prev.filter(p => p.id !== id));
    } catch (err) {
      setError(err as Error);
    }
  }, []);

  const submitProposal = useCallback(async (id: string) => {
    await updateProposal(id, { status: 'submitted' });
  }, [updateProposal]);

  return {
    proposals,
    isLoading,
    error,
    createProposal,
    updateProposal,
    deleteProposal,
    submitProposal
  };
};
