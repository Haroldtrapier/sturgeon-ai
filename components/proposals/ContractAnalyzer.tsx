import React, { useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

interface AnalysisResult {
  complexity: 'low' | 'medium' | 'high';
  keyRequirements: string[];
  deadlines: { item: string; date: string }[];
  risks: { level: string; description: string }[];
  recommendations: string[];
  complianceIssues: string[];
}

interface ContractAnalyzerProps {
  contractText: string;
  onAnalyze: (text: string) => Promise<AnalysisResult>;
}

export const ContractAnalyzer: React.FC<ContractAnalyzerProps> = ({
  contractText,
  onAnalyze
}) => {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    try {
      const result = await onAnalyze(contractText);
      setAnalysis(result);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'low': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'high': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-900">Contract Analysis</h2>
          <Button
            onClick={handleAnalyze}
            disabled={isAnalyzing || !contractText}
            variant="primary"
          >
            {isAnalyzing ? 'Analyzing...' : '🔍 Analyze Contract'}
          </Button>
        </div>
      </Card>

      {analysis && (
        <>
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">Complexity Assessment</h3>
              <span className={`px-4 py-2 rounded-full font-semibold uppercase text-sm ${getComplexityColor(analysis.complexity)}`}>
                {analysis.complexity}
              </span>
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Key Requirements</h3>
            <ul className="space-y-2">
              {analysis.keyRequirements.map((req, idx) => (
                <li key={idx} className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  <span className="text-gray-700">{req}</span>
                </li>
              ))}
            </ul>
          </Card>

          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Critical Deadlines</h3>
            <div className="space-y-3">
              {analysis.deadlines.map((deadline, idx) => (
                <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="font-medium text-gray-900">{deadline.item}</span>
                  <span className="text-sm text-gray-600">{deadline.date}</span>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Risk Assessment</h3>
            <div className="space-y-3">
              {analysis.risks.map((risk, idx) => (
                <div key={idx} className="border-l-4 border-red-500 pl-4 py-2">
                  <span className="font-semibold text-red-700">{risk.level}:</span>
                  <p className="text-gray-700 mt-1">{risk.description}</p>
                </div>
              ))}
            </div>
          </Card>

          {analysis.complianceIssues.length > 0 && (
            <Card className="p-6 border-red-200">
              <h3 className="text-lg font-semibold mb-4 text-red-700">Compliance Issues</h3>
              <ul className="space-y-2">
                {analysis.complianceIssues.map((issue, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-red-600 mr-2">⚠</span>
                    <span className="text-gray-700">{issue}</span>
                  </li>
                ))}
              </ul>
            </Card>
          )}

          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Recommendations</h3>
            <ul className="space-y-2">
              {analysis.recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start">
                  <span className="text-green-600 mr-2">✓</span>
                  <span className="text-gray-700">{rec}</span>
                </li>
              ))}
            </ul>
          </Card>
        </>
      )}
    </div>
  );
};
