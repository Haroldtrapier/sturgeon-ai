import React from 'react';
import { GrantCard } from './GrantCard';

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

interface GrantsListProps {
  grants: Grant[];
  savedGrantIds: Set<string>;
  onSaveGrant: (grantId: string) => void;
  onViewDetails: (grantId: string) => void;
  isLoading?: boolean;
}

export const GrantsList: React.FC<GrantsListProps> = ({
  grants,
  savedGrantIds,
  onSaveGrant,
  onViewDetails,
  isLoading = false
}) => {
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (grants.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No grants found. Try adjusting your filters.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {grants.map((grant) => (
        <GrantCard
          key={grant.id}
          grant={grant}
          isSaved={savedGrantIds.has(grant.id)}
          onSave={onSaveGrant}
          onViewDetails={onViewDetails}
        />
      ))}
    </div>
  );
};
