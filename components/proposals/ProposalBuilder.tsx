import React, { useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Textarea } from '@/components/ui/Textarea';
import { Input } from '@/components/ui/Input';

interface ProposalSection {
  id: string;
  title: string;
  content: string;
  wordCount: number;
  required: boolean;
  aiGenerated?: boolean;
}

interface ProposalBuilderProps {
  opportunityId?: string;
  sections: ProposalSection[];
  onSave: (sections: ProposalSection[]) => void;
  onGenerateWithAI: (sectionId: string) => Promise<string>;
}

export const ProposalBuilder: React.FC<ProposalBuilderProps> = ({
  opportunityId,
  sections: initialSections,
  onSave,
  onGenerateWithAI
}) => {
  const [sections, setSections] = useState<ProposalSection[]>(initialSections);
  const [activeSection, setActiveSection] = useState<string>(sections[0]?.id || '');
  const [isGenerating, setIsGenerating] = useState<string | null>(null);
  const [proposalTitle, setProposalTitle] = useState('Untitled Proposal');

  const updateSection = (sectionId: string, content: string) => {
    setSections(prev =>
      prev.map(section =>
        section.id === sectionId
          ? {
              ...section,
              content,
              wordCount: content.trim().split(/\s+/).length
            }
          : section
      )
    );
  };

  const handleAIGenerate = async (sectionId: string) => {
    setIsGenerating(sectionId);
    try {
      const generatedContent = await onGenerateWithAI(sectionId);
      setSections(prev =>
        prev.map(section =>
          section.id === sectionId
            ? {
                ...section,
                content: generatedContent,
                wordCount: generatedContent.trim().split(/\s+/).length,
                aiGenerated: true
              }
            : section
        )
      );
    } catch (error) {
      console.error('AI generation failed:', error);
    } finally {
      setIsGenerating(null);
    }
  };

  const activeContent = sections.find(s => s.id === activeSection);
  const totalWords = sections.reduce((sum, s) => sum + s.wordCount, 0);
  const completedSections = sections.filter(s => s.content.trim().length > 0).length;

  return (
    <div className="flex gap-6 h-full">
      {/* Sidebar - Section Navigation */}
      <div className="w-64 bg-white rounded-lg shadow-md p-4">
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Proposal Sections</h2>
          <p className="text-sm text-gray-500 mt-1">
            {completedSections}/{sections.length} completed
          </p>
        </div>

        <div className="space-y-2">
          {sections.map(section => (
            <button
              key={section.id}
              onClick={() => setActiveSection(section.id)}
              className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
                activeSection === section.id
                  ? 'bg-blue-100 text-blue-700'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm">{section.title}</span>
                {section.content.trim() ? (
                  <span className="text-green-600">✓</span>
                ) : section.required ? (
                  <span className="text-red-500">*</span>
                ) : null}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {section.wordCount} words
              </div>
            </button>
          ))}
        </div>

        <div className="mt-6 pt-4 border-t border-gray-200">
          <Button
            onClick={() => onSave(sections)}
            variant="primary"
            className="w-full"
          >
            Save Proposal
          </Button>
        </div>
      </div>

      {/* Main Editor */}
      <div className="flex-1">
        <Card className="p-6 h-full flex flex-col">
          <div className="mb-4">
            <Input
              type="text"
              value={proposalTitle}
              onChange={(e) => setProposalTitle(e.target.value)}
              className="text-2xl font-bold border-none focus:ring-0"
              placeholder="Proposal Title"
            />
          </div>

          {activeContent && (
            <>
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">
                    {activeContent.title}
                    {activeContent.required && <span className="text-red-500 ml-1">*</span>}
                  </h3>
                  {activeContent.aiGenerated && (
                    <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded mt-1 inline-block">
                      AI Generated
                    </span>
                  )}
                </div>
                <Button
                  onClick={() => handleAIGenerate(activeContent.id)}
                  disabled={isGenerating === activeContent.id}
                  variant="outline"
                >
                  {isGenerating === activeContent.id ? (
                    <>
                      <span className="animate-spin mr-2">⚡</span>
                      Generating...
                    </>
                  ) : (
                    <>🤖 Generate with AI</>
                  )}
                </Button>
              </div>

              <Textarea
                value={activeContent.content}
                onChange={(e) => updateSection(activeContent.id, e.target.value)}
                placeholder={`Write your ${activeContent.title.toLowerCase()} here...`}
                className="flex-1 min-h-[400px] font-mono"
              />

              <div className="mt-4 flex justify-between text-sm text-gray-500">
                <span>Word count: {activeContent.wordCount}</span>
                <span>Total proposal: {totalWords} words</span>
              </div>
            </>
          )}
        </Card>
      </div>
    </div>
  );
};
