'use client';

import { useState, useEffect } from 'react';
import { Heart, ExternalLink, Calendar, DollarSign, Building } from 'lucide-react';

export default function SavedOpportunitiesPage() {
  const [saved, setSaved] = useState([
    {
      id: '1',
      title: 'IT Modernization Services',
      agency: 'Department of Defense',
      value: '$5.2M',
      deadline: '2024-02-15',
      status: 'Active',
      matchScore: 95,
      savedDate: '2024-01-10',
    },
    {
      id: '2',
      title: 'Cybersecurity Assessment',
      agency: 'Department of Homeland Security',
      value: '$2.8M',
      deadline: '2024-02-20',
      status: 'Active',
      matchScore: 88,
      savedDate: '2024-01-12',
    },
  ]);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Saved Opportunities</h1>
        <p className="text-slate-600">{saved.length} opportunities saved for later</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex gap-4">
          <select className="px-4 py-2 border border-slate-300 rounded-lg">
            <option>All Agencies</option>
            <option>DOD</option>
            <option>DHS</option>
            <option>GSA</option>
          </select>
          <select className="px-4 py-2 border border-slate-300 rounded-lg">
            <option>All Status</option>
            <option>Active</option>
            <option>Closing Soon</option>
          </select>
          <select className="px-4 py-2 border border-slate-300 rounded-lg">
            <option>Sort by: Match Score</option>
            <option>Sort by: Deadline</option>
            <option>Sort by: Value</option>
            <option>Sort by: Date Saved</option>
          </select>
        </div>
      </div>

      {/* Saved Opportunities List */}
      <div className="space-y-4">
        {saved.map((opp) => (
          <div key={opp.id} className="bg-white rounded-lg shadow p-6 border border-slate-200 hover:border-blue-300 transition">
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-xl font-semibold text-slate-900">{opp.title}</h3>
                  <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
                    {opp.status}
                  </span>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full font-semibold">
                    {opp.matchScore}% Match
                  </span>
                </div>
                <div className="flex gap-6 text-sm text-slate-600">
                  <div className="flex items-center gap-2">
                    <Building className="w-4 h-4" />
                    {opp.agency}
                  </div>
                  <div className="flex items-center gap-2">
                    <DollarSign className="w-4 h-4" />
                    {opp.value}
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="w-4 h-4" />
                    Deadline: {opp.deadline}
                  </div>
                </div>
              </div>
              <div className="flex gap-2">
                <button className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition">
                  <Heart className="w-5 h-5 fill-current" />
                </button>
                <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2">
                  View Details
                  <ExternalLink className="w-4 h-4" />
                </button>
              </div>
            </div>
            <div className="text-sm text-slate-500">
              Saved on {opp.savedDate}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
