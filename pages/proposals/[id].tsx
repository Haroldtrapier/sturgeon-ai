import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { ProposalBuilder } from '@/components/proposals/ProposalBuilder';
import { useProposals } from '@/hooks/useProposals';
import { aiAPI } from '@/services/aiAPI';

const DEFAULT_SECTIONS = [
  { id: 'executive_summary', title: 'Executive Summary', content: '', wordCount: 0, required: true },
  { id: 'technical_approach', title: 'Technical Approach', content: '', wordCount: 0, required: true },
  { id: 'management_plan', title: 'Management Plan', content: '', wordCount: 0, required: true },
  { id: 'budget', title: 'Budget Justification', content: '', wordCount: 0, required: true },
  { id: 'qualifications', title: 'Qualifications & Experience', content: '', wordCount: 0, required: true },
  { id: 'deliverables', title: 'Deliverables', content: '', wordCount: 0, required: false },
  { id: 'timeline', title: 'Project Timeline', content: '', wordCount: 0, required: false },
];

export default function ProposalEditorPage() {
  const router = useRouter();
  const { id } = router.query;
  const { proposals, updateProposal } = useProposals();

  const [sections, setSections] = useState(DEFAULT_SECTIONS);
  const [proposal, setProposal] = useState<any>(null);

  useEffect(() => {
    if (id && proposals) {
      const found = proposals.find(p => p.id === id);
      if (found) {
        setProposal(found);
        // Load sections from database if available
        // For now, using default sections
      }
    }
  }, [id, proposals]);

  const handleSave = async (updatedSections: any[]) => {
    if (!id) return;

    try {
      await updateProposal(id as string, {
        sections: updatedSections,
        total_word_count: updatedSections.reduce((sum, s) => sum + s.wordCount, 0)
      });
      alert('Proposal saved successfully!');
    } catch (error) {
      console.error('Failed to save proposal:', error);
      alert('Failed to save proposal');
    }
  };

  const handleGenerateWithAI = async (sectionId: string): Promise<string> => {
    try {
      const content = await aiAPI.generateProposalSection({
        sectionId,
        context: {
          opportunityId: proposal?.opportunity_id,
          previousSections: sections
            .filter(s => s.content && s.order_index < sections.find(sec => sec.id === sectionId)?.order_index)
            .map(s => s.content),
          requirements: []
        }
      });
      return content;
    } catch (error) {
      console.error('AI generation failed:', error);
      throw error;
    }
  };

  return (
    <>
      <Head>
        <title>Proposal Builder - Sturgeon AI</title>
      </Head>

      <div className="min-h-screen bg-gray-50">
        <div className="max-w-[1600px] mx-auto px-4 py-6">
          <ProposalBuilder
            opportunityId={proposal?.opportunity_id}
            sections={sections}
            onSave={handleSave}
            onGenerateWithAI={handleGenerateWithAI}
          />
        </div>
      </div>
    </>
  );
}
