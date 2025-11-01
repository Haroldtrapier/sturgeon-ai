'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Wand2, FileText, Download } from 'lucide-react';

export default function ProposalsPage() {
  const router = useRouter();
  const [contractId, setContractId] = useState('');
  const [requirements, setRequirements] = useState('');
  const [proposal, setProposal] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    const isAuth = localStorage.getItem('isAuthenticated');
    if (!isAuth) {
      router.push('/login');
    }
  }, [router]);

  const generateProposal = async () => {
    setIsGenerating(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://sturgeon-ai-prod.vercel.app';
      const response = await axios.post(`${apiUrl}/api/ai/generate-proposal`, {
        contract_id: contractId,
        requirements: requirements
      });
      setProposal(response.data.proposal || '');
    } catch (error) {
      console.error('Error generating proposal:', error);
      // Mock response for demo
      setProposal(`# Proposal for Contract ${contractId}

## Executive Summary
Our organization is pleased to submit this proposal in response to your requirements for ${requirements || 'advanced technology solutions'}. With proven expertise and a track record of successful government contracts, we are uniquely positioned to deliver exceptional results.

## Technical Approach
1. **Solution Architecture**: Cloud-native, scalable infrastructure
2. **Security**: FISMA compliant, FedRAMP authorized
3. **Innovation**: AI-powered automation and analytics
4. **Support**: 24/7 dedicated support team

## Team Qualifications
- 15+ years government contracting experience
- CMMI Level 3 certified
- ISO 27001 certified
- Cleared personnel available

## Pricing
Competitive pricing with flexible payment terms aligned with government fiscal year requirements.

## Conclusion
We are committed to delivering excellence and exceeding expectations on this critical project.`);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-blue-600">Sturgeon AI</h1>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold">Proposal Builder</h2>
          <p className="mt-2 text-gray-600">AI-powered proposal generation</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Input Requirements</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Contract ID</label>
                <Input
                  placeholder="e.g., DOD-2024-001"
                  value={contractId}
                  onChange={(e) => setContractId(e.target.value)}
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Requirements</label>
                <Textarea
                  placeholder="Enter contract requirements..."
                  rows={10}
                  value={requirements}
                  onChange={(e) => setRequirements(e.target.value)}
                />
              </div>
              <Button 
                onClick={generateProposal} 
                disabled={isGenerating}
                className="w-full"
              >
                <Wand2 className="h-4 w-4 mr-2" />
                {isGenerating ? 'Generating...' : 'Generate Proposal'}
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Generated Proposal</CardTitle>
              {proposal && (
                <Button size="sm" variant="outline">
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              )}
            </CardHeader>
            <CardContent>
              {proposal ? (
                <div className="prose max-w-none">
                  <pre className="whitespace-pre-wrap text-sm">{proposal}</pre>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                  <FileText className="h-12 w-12 mb-4" />
                  <p>Your generated proposal will appear here</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
