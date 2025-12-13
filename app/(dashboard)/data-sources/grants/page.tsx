'use client';

import { useState } from 'react';
import { Gift, Calendar, Building, DollarSign } from 'lucide-react';

export default function GrantsGovPage() {
  const [grants] = useState([
    {
      id: '1',
      opportunityNumber: 'EPA-R-EPA-ORD-23-03',
      title: 'Environmental Research and Development',
      agency: 'Environmental Protection Agency',
      eligibility: 'Universities, Non-profits',
      fundingAmount: '$2M - $5M',
      deadline: '2024-03-15',
      category: 'Research',
    },
    {
      id: '2',
      opportunityNumber: 'HHS-2024-ACF-OCS-EH-0001',
      title: 'Community Health Services',
      agency: 'Department of Health and Human Services',
      eligibility: 'State/Local Governments, Non-profits',
      fundingAmount: '$500K - $1.5M',
      deadline: '2024-02-28',
      category: 'Healthcare',
    },
  ]);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Grants.gov Integration</h1>
        <p className="text-slate-600">Federal grant opportunities and funding</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Gift className="w-8 h-8 text-blue-600" />
            <h3 className="text-2xl font-bold">3,245</h3>
          </div>
          <p className="text-slate-600 text-sm">Active Grants</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <DollarSign className="w-8 h-8 text-green-600" />
            <h3 className="text-2xl font-bold">$85B</h3>
          </div>
          <p className="text-slate-600 text-sm">Available Funding</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Building className="w-8 h-8 text-purple-600" />
            <h3 className="text-2xl font-bold">26</h3>
          </div>
          <p className="text-slate-600 text-sm">Federal Agencies</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Calendar className="w-8 h-8 text-orange-600" />
            <h3 className="text-2xl font-bold">145</h3>
          </div>
          <p className="text-slate-600 text-sm">Closing This Month</p>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Search Grants</h3>
        <div className="grid grid-cols-3 gap-4 mb-4">
          <input
            type="text"
            placeholder="Keyword search..."
            className="px-4 py-2 border border-slate-300 rounded-lg"
          />
          <select className="px-4 py-2 border border-slate-300 rounded-lg">
            <option>All Categories</option>
            <option>Research</option>
            <option>Healthcare</option>
            <option>Education</option>
            <option>Environment</option>
          </select>
          <select className="px-4 py-2 border border-slate-300 rounded-lg">
            <option>All Agencies</option>
            <option>EPA</option>
            <option>HHS</option>
            <option>DOE</option>
            <option>NSF</option>
          </select>
        </div>
        <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
          Search Grants
        </button>
      </div>

      {/* Grant Opportunities */}
      <div className="space-y-4">
        {grants.map((grant) => (
          <div key={grant.id} className="bg-white rounded-lg shadow p-6 border border-slate-200">
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-xl font-semibold text-slate-900">{grant.title}</h3>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                    {grant.category}
                  </span>
                </div>
                <p className="text-sm text-slate-600 mb-3">{grant.opportunityNumber}</p>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center gap-2 text-slate-600">
                    <Building className="w-4 h-4" />
                    {grant.agency}
                  </div>
                  <div className="flex items-center gap-2 text-slate-600">
                    <DollarSign className="w-4 h-4" />
                    {grant.fundingAmount}
                  </div>
                  <div className="flex items-center gap-2 text-slate-600">
                    <Calendar className="w-4 h-4" />
                    Deadline: {grant.deadline}
                  </div>
                  <div className="text-slate-600">
                    Eligible: {grant.eligibility}
                  </div>
                </div>
              </div>
              <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
