import React from 'react';
import { Card } from '@/components/ui/Card';

interface AnalyticsData {
  totalOpportunities: number;
  savedOpportunities: number;
  proposalsInProgress: number;
  proposalsSubmitted: number;
  successRate: number;
  avgResponseTime: number;
  topCategories: { name: string; count: number }[];
  recentActivity: { action: string; timestamp: string }[];
}

interface AnalyticsDashboardProps {
  data: AnalyticsData;
  timeRange: 'week' | 'month' | 'quarter' | 'year';
  onTimeRangeChange: (range: string) => void;
}

export const AnalyticsDashboard: React.FC<AnalyticsDashboardProps> = ({
  data,
  timeRange,
  onTimeRangeChange
}) => {
  return (
    <div className="space-y-6">
      {/* Time Range Selector */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
        <select
          value={timeRange}
          onChange={(e) => onTimeRangeChange(e.target.value)}
          className="border border-gray-300 rounded-md px-4 py-2"
        >
          <option value="week">Last 7 Days</option>
          <option value="month">Last 30 Days</option>
          <option value="quarter">Last Quarter</option>
          <option value="year">Last Year</option>
        </select>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-4 gap-4">
        <Card className="p-6">
          <div className="text-sm text-gray-600 mb-1">Total Opportunities</div>
          <div className="text-3xl font-bold text-gray-900">{data.totalOpportunities}</div>
        </Card>

        <Card className="p-6">
          <div className="text-sm text-gray-600 mb-1">Saved Opportunities</div>
          <div className="text-3xl font-bold text-blue-600">{data.savedOpportunities}</div>
        </Card>

        <Card className="p-6">
          <div className="text-sm text-gray-600 mb-1">Proposals In Progress</div>
          <div className="text-3xl font-bold text-yellow-600">{data.proposalsInProgress}</div>
        </Card>

        <Card className="p-6">
          <div className="text-sm text-gray-600 mb-1">Proposals Submitted</div>
          <div className="text-3xl font-bold text-green-600">{data.proposalsSubmitted}</div>
        </Card>
      </div>

      {/* Performance Metrics */}
      <div className="grid grid-cols-2 gap-4">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Success Rate</h3>
          <div className="flex items-center justify-center">
            <div className="relative w-32 h-32">
              <svg className="transform -rotate-90 w-32 h-32">
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="#e5e7eb"
                  strokeWidth="12"
                  fill="none"
                />
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="#10b981"
                  strokeWidth="12"
                  fill="none"
                  strokeDasharray={`${2 * Math.PI * 56 * (data.successRate / 100)} ${2 * Math.PI * 56}`}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-2xl font-bold text-gray-900">{data.successRate}%</span>
              </div>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Avg Response Time</h3>
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-600">{data.avgResponseTime}</div>
            <div className="text-sm text-gray-600 mt-2">days</div>
          </div>
        </Card>
      </div>

      {/* Top Categories */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Top Categories</h3>
        <div className="space-y-3">
          {data.topCategories.map((category, idx) => (
            <div key={idx}>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-gray-700">{category.name}</span>
                <span className="text-gray-600">{category.count}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full"
                  style={{
                    width: `${(category.count / Math.max(...data.topCategories.map(c => c.count))) * 100}%`
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Recent Activity */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
        <div className="space-y-3">
          {data.recentActivity.map((activity, idx) => (
            <div key={idx} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
              <span className="text-sm text-gray-700">{activity.action}</span>
              <span className="text-xs text-gray-500">{new Date(activity.timestamp).toLocaleString()}</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
