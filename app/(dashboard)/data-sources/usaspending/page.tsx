'use client';

import { useState } from 'react';
import { DollarSign, TrendingUp, PieChart, Download } from 'lucide-react';

export default function USASpendingPage() {
  const [spending] = useState([
    {
      agency: 'Department of Defense',
      fy2024: '$742B',
      fy2023: '$726B',
      change: '+2.2%',
      topCategories: ['IT Services', 'R&D', 'Facilities'],
    },
    {
      agency: 'Department of Health and Human Services',
      fy2024: '$1.7T',
      fy2023: '$1.6T',
      change: '+6.3%',
      topCategories: ['Healthcare', 'Research', 'Administration'],
    },
    {
      agency: 'Department of Homeland Security',
      fy2024: '$102B',
      fy2023: '$97B',
      change: '+5.2%',
      topCategories: ['Security', 'IT', 'Operations'],
    },
  ]);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">USASpending.gov Integration</h1>
        <p className="text-slate-600">Federal spending data and analytics</p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <DollarSign className="w-8 h-8 text-green-600" />
            <h3 className="text-2xl font-bold">$6.1T</h3>
          </div>
          <p className="text-slate-600 text-sm">Total Federal Spending (FY24)</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="w-8 h-8 text-blue-600" />
            <h3 className="text-2xl font-bold">+4.8%</h3>
          </div>
          <p className="text-slate-600 text-sm">YoY Growth</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <PieChart className="w-8 h-8 text-purple-600" />
            <h3 className="text-2xl font-bold">425K</h3>
          </div>
          <p className="text-slate-600 text-sm">Active Awards</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Download className="w-8 h-8 text-orange-600" />
            <h3 className="text-2xl font-bold">Real-time</h3>
          </div>
          <p className="text-slate-600 text-sm">Data Updates</p>
        </div>
      </div>

      {/* Agency Spending */}
      <div className="bg-white rounded-lg shadow mb-8">
        <div className="px-6 py-4 border-b border-slate-200 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-slate-900">Top Spending Agencies</h3>
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold flex items-center gap-2">
            <Download className="w-4 h-4" />
            Export Data
          </button>
        </div>
        <div className="p-6">
          <div className="space-y-6">
            {spending.map((agency, idx) => (
              <div key={idx} className="border border-slate-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h4 className="font-semibold text-slate-900 mb-1">{agency.agency}</h4>
                    <div className="flex gap-2">
                      {agency.topCategories.map((cat, i) => (
                        <span key={i} className="px-2 py-1 bg-slate-100 text-slate-700 text-xs rounded">
                          {cat}
                        </span>
                      ))}
                    </div>
                  </div>
                  <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-semibold rounded-full">
                    {agency.change}
                  </span>
                </div>
                <div className="flex gap-8 text-sm">
                  <div>
                    <p className="text-slate-600">FY 2024</p>
                    <p className="text-xl font-bold text-slate-900">{agency.fy2024}</p>
                  </div>
                  <div>
                    <p className="text-slate-600">FY 2023</p>
                    <p className="text-lg font-semibold text-slate-700">{agency.fy2023}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Search */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow p-6 text-white">
        <h3 className="text-xl font-semibold mb-3">Search USASpending Data</h3>
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="Search by agency, program, contractor..."
            className="flex-1 px-4 py-3 rounded-lg text-slate-900"
          />
          <button className="px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-slate-100">
            Search
          </button>
        </div>
      </div>
    </div>
  );
}
