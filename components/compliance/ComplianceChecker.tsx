import React, { useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

interface ComplianceCheck {
  id: string;
  category: string;
  requirement: string;
  status: 'passed' | 'failed' | 'warning' | 'pending';
  details: string;
  reference: string;
}

interface ComplianceReport {
  overallStatus: 'compliant' | 'non-compliant' | 'needs-review';
  score: number;
  checks: ComplianceCheck[];
  recommendations: string[];
}

interface ComplianceCheckerProps {
  documentId: string;
  regulationType: 'FAR' | 'DFARS' | 'FISMA' | 'CMMC' | 'ALL';
  onRunCheck: (docId: string, regType: string) => Promise<ComplianceReport>;
}

export const ComplianceChecker: React.FC<ComplianceCheckerProps> = ({
  documentId,
  regulationType,
  onRunCheck
}) => {
  const [report, setReport] = useState<ComplianceReport | null>(null);
  const [isChecking, setIsChecking] = useState(false);

  const handleRunCheck = async () => {
    setIsChecking(true);
    try {
      const result = await onRunCheck(documentId, regulationType);
      setReport(result);
    } catch (error) {
      console.error('Compliance check failed:', error);
    } finally {
      setIsChecking(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'passed': return 'text-green-700 bg-green-100';
      case 'failed': return 'text-red-700 bg-red-100';
      case 'warning': return 'text-yellow-700 bg-yellow-100';
      default: return 'text-gray-700 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'passed': return '✓';
      case 'failed': return '✗';
      case 'warning': return '⚠';
      default: return '○';
    }
  };

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Compliance Checker</h2>
            <p className="text-sm text-gray-600 mt-1">
              Checking against: {regulationType === 'ALL' ? 'All Regulations' : regulationType}
            </p>
          </div>
          <Button
            onClick={handleRunCheck}
            disabled={isChecking}
            variant="primary"
          >
            {isChecking ? 'Running Checks...' : '🔒 Run Compliance Check'}
          </Button>
        </div>
      </Card>

      {report && (
        <>
          {/* Overall Score */}
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold">Overall Compliance Score</h3>
                <p className="text-sm text-gray-600 mt-1">
                  {report.overallStatus === 'compliant' && 'Your document meets all compliance requirements'}
                  {report.overallStatus === 'non-compliant' && 'Critical issues found - action required'}
                  {report.overallStatus === 'needs-review' && 'Some items require manual review'}
                </p>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600">{report.score}%</div>
                <div className={`mt-2 px-4 py-1 rounded-full text-sm font-semibold ${
                  report.overallStatus === 'compliant' ? 'bg-green-100 text-green-700' :
                  report.overallStatus === 'non-compliant' ? 'bg-red-100 text-red-700' :
                  'bg-yellow-100 text-yellow-700'
                }`}>
                  {report.overallStatus.toUpperCase()}
                </div>
              </div>
            </div>
          </Card>

          {/* Compliance Checks */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Detailed Checks</h3>
            <div className="space-y-3">
              {report.checks.map((check) => (
                <div key={check.id} className="border rounded-lg p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className={`px-2 py-1 rounded text-sm font-semibold ${getStatusColor(check.status)}`}>
                          {getStatusIcon(check.status)} {check.status.toUpperCase()}
                        </span>
                        <span className="text-xs text-gray-500">{check.category}</span>
                      </div>
                      <h4 className="font-semibold text-gray-900">{check.requirement}</h4>
                      <p className="text-sm text-gray-600 mt-1">{check.details}</p>
                      {check.reference && (
                        <p className="text-xs text-blue-600 mt-2">Reference: {check.reference}</p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Recommendations */}
          {report.recommendations.length > 0 && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Recommendations</h3>
              <ul className="space-y-2">
                {report.recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-blue-600 mr-2">→</span>
                    <span className="text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </Card>
          )}
        </>
      )}
    </div>
  );
};
