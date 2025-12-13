'use client';

import { useState } from 'react';
import { Zap, Target, Award, TrendingUp } from 'lucide-react';

export default function MatchingPage() {
  const [matches] = useState([
    {
      id: '1',
      title: 'Enterprise Cloud Migration Services',
      agency: 'Department of Veterans Affairs',
      matchScore: 97,
      matchReasons: [
        'Past performance in cloud migration',
        'VA contract history',
        'Security clearances aligned',
        'Technical capabilities match'
      ],
      value: '$8.5M',
      deadline: '2024-03-01',
      confidence: 'Very High',
    },
    {
      id: '2',
      title: 'AI-Powered Data Analytics Platform',
      agency: 'Department of Defense',
      matchScore: 94,
      matchReasons: [
        'AI/ML expertise',
        'DOD experience',
        'Top Secret clearance',
        'Similar project delivered'
      ],
      value: '$12.3M',
      deadline: '2024-02-25',
      confidence: 'High',
    },
  ]);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">AI Contract Matching</h1>
        <p className="text-slate-600">Opportunities matched to your company profile and capabilities</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Zap className="w-8 h-8 text-blue-600" />
            <h3 className="text-2xl font-bold">{matches.length}</h3>
          </div>
          <p className="text-slate-600 text-sm">High Matches This Week</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Target className="w-8 h-8 text-green-600" />
            <h3 className="text-2xl font-bold">95%</h3>
          </div>
          <p className="text-slate-600 text-sm">Avg Match Score</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Award className="w-8 h-8 text-purple-600" />
            <h3 className="text-2xl font-bold">$45M</h3>
          </div>
          <p className="text-slate-600 text-sm">Total Opportunity Value</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="w-8 h-8 text-orange-600" />
            <h3 className="text-2xl font-bold">32%</h3>
          </div>
          <p className="text-slate-600 text-sm">Win Rate on Matches</p>
        </div>
      </div>

      {/* Matches */}
      <div className="space-y-6">
        {matches.map((match) => (
          <div key={match.id} className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-green-500">
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-xl font-semibold text-slate-900">{match.title}</h3>
                  <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-bold rounded-full">
                    {match.matchScore}% Match
                  </span>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                    {match.confidence} Confidence
                  </span>
                </div>
                <p className="text-slate-600 mb-3">{match.agency} • {match.value} • Deadline: {match.deadline}</p>

                <div className="bg-slate-50 rounded-lg p-4 mb-4">
                  <h4 className="font-semibold text-slate-900 mb-2">Why This Matches:</h4>
                  <ul className="space-y-1">
                    {match.matchReasons.map((reason, idx) => (
                      <li key={idx} className="text-sm text-slate-700 flex items-start gap-2">
                        <span className="text-green-600 mt-0.5">✓</span>
                        {reason}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
                Start Proposal
              </button>
              <button className="px-6 py-2 border border-slate-300 rounded-lg hover:bg-slate-50">
                View Full Details
              </button>
              <button className="px-6 py-2 border border-slate-300 rounded-lg hover:bg-slate-50">
                Save for Later
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
