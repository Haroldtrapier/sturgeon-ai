import React, { useState } from 'react';
import Head from 'next/head';
import { GrantsList } from '@/components/grants/GrantsList';
import { GrantSearchFilters } from '@/components/grants/GrantSearchFilters';
import { useOpportunities } from '@/hooks/useOpportunities';
import { grantsAPI } from '@/services/grantsAPI';

export default function OpportunitiesPage() {
  const { opportunities, isLoading, fetchOpportunities, saveOpportunity } = useOpportunities();
  const [savedGrantIds, setSavedGrantIds] = useState<Set<string>>(new Set());
  const [selectedGrant, setSelectedGrant] = useState<string | null>(null);

  const handleSearch = async (filters: any) => {
    await fetchOpportunities(filters);
  };

  const handleReset = async () => {
    await fetchOpportunities({});
  };

  const handleSaveGrant = async (grantId: string) => {
    try {
      await saveOpportunity(grantId);
      setSavedGrantIds(prev => new Set([...prev, grantId]));
    } catch (error) {
      console.error('Failed to save grant:', error);
    }
  };

  const handleViewDetails = (grantId: string) => {
    setSelectedGrant(grantId);
    // Could open modal or navigate to detail page
    window.location.href = `/opportunities/${grantId}`;
  };

  const handleSync = async () => {
    try {
      const result = await grantsAPI.syncFromGrantsGov();
      alert(`Synced ${result.synced} grants successfully!`);
      await fetchOpportunities({});
    } catch (error) {
      console.error('Sync failed:', error);
      alert('Failed to sync grants. Check console for details.');
    }
  };

  return (
    <>
      <Head>
        <title>Opportunities - Sturgeon AI</title>
      </Head>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Grant Opportunities
              </h1>
              <p className="mt-2 text-sm text-gray-600">
                Discover and track government grants and contracts
              </p>
            </div>
            <button
              onClick={handleSync}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              🔄 Sync from Grants.gov
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Filters Sidebar */}
            <div className="lg:col-span-1">
              <GrantSearchFilters
                onSearch={handleSearch}
                onReset={handleReset}
              />
            </div>

            {/* Grants List */}
            <div className="lg:col-span-3">
              <GrantsList
                grants={opportunities}
                savedGrantIds={savedGrantIds}
                onSaveGrant={handleSaveGrant}
                onViewDetails={handleViewDetails}
                isLoading={isLoading}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
