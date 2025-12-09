import React from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

interface Grant {
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

interface GrantCardProps {
  grant: Grant;
  onSave?: (grantId: string) => void;
  onViewDetails?: (grantId: string) => void;
  isSaved?: boolean;
}

export const GrantCard: React.FC<GrantCardProps> = ({
  grant,
  onSave,
  onViewDetails,
  isSaved = false
}) => {
  const deadlineDate = new Date(grant.deadline);
  const daysUntilDeadline = Math.ceil((deadlineDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24));
  const isUrgent = daysUntilDeadline <= 14;

  return (
    <Card className="p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-gray-900 mb-2">{grant.title}</h3>
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span className="font-medium">{grant.agency}</span>
            <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">
              {grant.category}
            </span>
          </div>
        </div>
        {grant.matchScore && (
          <div className="flex flex-col items-center ml-4">
            <div className="text-2xl font-bold text-green-600">{grant.matchScore}%</div>
            <div className="text-xs text-gray-500">Match</div>
          </div>
        )}
      </div>

      <p className="text-gray-700 mb-4 line-clamp-3">{grant.description}</p>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <span className="text-sm text-gray-500">Award Amount</span>
          <p className="font-semibold text-lg text-gray-900">{grant.amount}</p>
        </div>
        <div>
          <span className="text-sm text-gray-500">Deadline</span>
          <p className={`font-semibold ${isUrgent ? 'text-red-600' : 'text-gray-900'}`}>
            {deadlineDate.toLocaleDateString()}
            {isUrgent && <span className="ml-2 text-xs">({daysUntilDeadline}d left)</span>}
          </p>
        </div>
      </div>

      {grant.eligibility && grant.eligibility.length > 0 && (
        <div className="mb-4">
          <span className="text-sm text-gray-500">Eligibility:</span>
          <div className="flex flex-wrap gap-2 mt-1">
            {grant.eligibility.slice(0, 3).map((item, idx) => (
              <span key={idx} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                {item}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="flex gap-2">
        <Button
          onClick={() => onViewDetails?.(grant.id)}
          className="flex-1"
          variant="primary"
        >
          View Details
        </Button>
        <Button
          onClick={() => onSave?.(grant.id)}
          variant={isSaved ? "secondary" : "outline"}
        >
          {isSaved ? '✓ Saved' : 'Save'}
        </Button>
      </div>
    </Card>
  );
};
