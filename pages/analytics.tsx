import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { AnalyticsDashboard } from '@/components/analytics/AnalyticsDashboard';
import { supabase } from '@/lib/supabase';

export default function AnalyticsPage() {
  const [analyticsData, setAnalyticsData] = useState({
    totalOpportunities: 0,
    savedOpportunities: 0,
    proposalsInProgress: 0,
    proposalsSubmitted: 0,
    successRate: 0,
    avgResponseTime: 0,
    topCategories: [],
    recentActivity: []
  });
  const [timeRange, setTimeRange] = useState<'week' | 'month' | 'quarter' | 'year'>('month');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    setIsLoading(true);
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;

      // Fetch various metrics
      const [opportunities, savedGrants, proposals, events] = await Promise.all([
        supabase.from('opportunities').select('*', { count: 'exact' }),
        supabase.from('saved_grants').select('*', { count: 'exact' }).eq('user_id', user.id),
        supabase.from('proposals').select('*').eq('user_id', user.id),
        supabase.from('analytics_events').select('*').eq('user_id', user.id).order('created_at', { ascending: false }).limit(10)
      ]);

      const proposalsData = proposals.data || [];
      const inProgress = proposalsData.filter(p => ['draft', 'in-progress', 'review'].includes(p.status)).length;
      const submitted = proposalsData.filter(p => p.status === 'submitted').length;
      const approved = proposalsData.filter(p => p.status === 'approved').length;

      setAnalyticsData({
        totalOpportunities: opportunities.count || 0,
        savedOpportunities: savedGrants.count || 0,
        proposalsInProgress: inProgress,
        proposalsSubmitted: submitted,
        successRate: submitted > 0 ? Math.round((approved / submitted) * 100) : 0,
        avgResponseTime: 7, // Calculate from actual data
        topCategories: [
          { name: 'Research', count: 45 },
          { name: 'Technology', count: 32 },
          { name: 'Infrastructure', count: 28 },
          { name: 'Education', count: 18 },
          { name: 'Health', count: 12 }
        ],
        recentActivity: (events.data || []).map(e => ({
          action: e.event_type,
          timestamp: e.created_at
        }))
      });
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>Analytics - Sturgeon AI</title>
      </Head>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnalyticsDashboard
            data={analyticsData}
            timeRange={timeRange}
            onTimeRangeChange={(range) => setTimeRange(range as any)}
          />
        </div>
      </div>
    </>
  );
}
