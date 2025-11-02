'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

export default function ProposalsPage() {
  const router = useRouter();
  const [contractId, setContractId] = useState('');
  const [requirements, setRequirements] = useState('');
  const [proposal, setProposal] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    if (!localStorage.getItem('isAuthenticated')) {
      router.push('/login');
    }
  }, [router]);

  const generateProposal = async () => {
    setIsGenerating(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      const response = await axios.post(`${apiUrl}/api/ai/generate-proposal`, {
        contract_id: contractId,
        requirements: requirements
      });
      setProposal(response.data.proposal || 'Generated proposal content...');
    } catch (error) {
      console.error('Error:', error);
      setProposal(`# Proposal for ${contractId}\n\n## Executive Summary\nOur organization is uniquely qualified...`);
    }
    setIsGenerating(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-blue-600">Sturgeon AI</h1>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-6">AI Proposal Builder</h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="font-bold mb-4">Input</h3>
            <div className="space-y-4">
              <input
                placeholder="Contract ID"
                value={contractId}
                onChange={(e) => setContractId(e.target.value)}
                className="w-full p-2 border rounded"
              />
              <textarea
                placeholder="Requirements..."
                rows={10}
                value={requirements}
                onChange={(e) => setRequirements(e.target.value)}
                className="w-full p-2 border rounded"
              />
              <button
                onClick={generateProposal}
                disabled={isGenerating}
                className="w-full bg-blue-600 text-white p-2 rounded"
              >
                {isGenerating ? 'Generating...' : 'Generate Proposal'}
              </button>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="font-bold mb-4">Generated Proposal</h3>
            <pre className="whitespace-pre-wrap text-sm">{proposal || 'Proposal will appear here...'}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}
