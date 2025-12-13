'use client';

import { useState } from 'react';
import { Eye, Bell, Calendar, TrendingUp } from 'lucide-react';

export default function WatchlistPage() {
  const [watchlist] = useState([
    {
      id: '1',
      keyword: 'Cybersecurity',
      matches: 45,
      newToday: 3,
      agencies: ['DOD', 'DHS', 'GSA'],
      avgValue: '$3.2M',
      alerts: true,
    },
    {
      id: '2',
      keyword: 'Cloud Infrastructure',
      matches: 32,
      newToday: 1,
      agencies: ['GSA', 'VA', 'DOD'],
      avgValue: '$4.5M',
      alerts: true,
    },
    {
      id: '3',
      keyword: 'AI/ML Services',
      matches: 18,
      newToday: 0,
      agencies: ['DOD', 'NASA', 'USDA'],
      avgValue: '$2.1M',
      alerts: false,
    },
  ]);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Watchlist</h1>
        <p className="text-slate-600">Monitor specific keywords and topics</p>
      </div>

      {/* Add New Watch */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow p-6 mb-6 text-white">
        <h3 className="text-xl font-semibold mb-3">Add New Watch</h3>
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="Enter keywords (e.g., 'Data Analytics', 'IT Security')"
            className="flex-1 px-4 py-2 rounded-lg text-slate-900"
          />
          <button className="px-6 py-2 bg-white text-blue-600 font-semibold rounded-lg hover:bg-slate-100 transition">
            Add to Watchlist
          </button>
        </div>
      </div>

      {/* Watchlist Items */}
      <div className="grid grid-cols-1 gap-6">
        {watchlist.map((item) => (
          <div key={item.id} className="bg-white rounded-lg shadow p-6 border border-slate-200">
            <div className="flex justify-between items-start mb-4">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-xl font-semibold text-slate-900">{item.keyword}</h3>
                  {item.newToday > 0 && (
                    <span className="px-3 py-1 bg-green-500 text-white text-sm rounded-full font-semibold">
                      {item.newToday} New Today
                    </span>
                  )}
                  {item.alerts && (
                    <Bell className="w-5 h-5 text-blue-600" />
                  )}
                </div>
                <div className="flex gap-6 text-sm text-slate-600">
                  <div className="flex items-center gap-2">
                    <Eye className="w-4 h-4" />
                    {item.matches} Total Matches
                  </div>
                  <div>
                    Agencies: {item.agencies.join(', ')}
                  </div>
                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-4 h-4" />
                    Avg Value: {item.avgValue}
                  </div>
                </div>
              </div>
              <div className="flex gap-2">
                <button className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50">
                  View Matches
                </button>
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  Configure
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
