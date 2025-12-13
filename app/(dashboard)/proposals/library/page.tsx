'use client';

import { useState } from 'react';
import { FileText, Calendar, Award, Eye } from 'lucide-react';

export default function ProposalLibraryPage() {
  const [proposals] = useState([
    {
      id: '1',
      title: 'DOD Cloud Infrastructure Modernization',
      rfpNumber: 'W52P1J-24-R-0015',
      status: 'Won',
      submittedDate: '2024-01-15',
      value: '$8.5M',
      score: 94,
    },
    {
      id: '2',
      title: 'DHS Cybersecurity Assessment Services',
      rfpNumber: 'HSHQDC-24-R-00023',
      status: 'Pending',
      submittedDate: '2024-01-20',
      value: '$4.2M',
      score: 88,
    },
    {
      id: '3',
      title: 'GSA IT Services BPA',
      rfpNumber: 'GS00Q-24-R-0042',
      status: 'Lost',
      submittedDate: '2023-12-10',
      value: '$12.3M',
      score: 76,
    },
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Won': return 'bg-green-100 text-green-800';
      case 'Pending': return 'bg-yellow-100 text-yellow-800';
      case 'Lost': return 'bg-red-100 text-red-800';
      default: return 'bg-slate-100 text-slate-800';
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Proposal Library</h1>
        <p className="text-slate-600">Access and manage all your past proposals</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <FileText className="w-8 h-8 text-blue-600" />
            <h3 className="text-2xl font-bold">{proposals.length}</h3>
          </div>
          <p className="text-slate-600 text-sm">Total Proposals</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Award className="w-8 h-8 text-green-600" />
            <h3 className="text-2xl font-bold">{proposals.filter(p => p.status === 'Won').length}</h3>
          </div>
          <p className="text-slate-600 text-sm">Wins</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Calendar className="w-8 h-8 text-purple-600" />
            <h3 className="text-2xl font-bold">{proposals.filter(p => p.status === 'Pending').length}</h3>
          </div>
          <p className="text-slate-600 text-sm">Pending</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Award className="w-8 h-8 text-orange-600" />
            <h3 className="text-2xl font-bold">33%</h3>
          </div>
          <p className="text-slate-600 text-sm">Win Rate</p>
        </div>
      </div>

      {/* Proposals Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Proposal</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">RFP Number</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Submitted</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Value</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {proposals.map((proposal) => (
              <tr key={proposal.id} className="hover:bg-slate-50">
                <td className="px-6 py-4">
                  <div className="font-semibold text-slate-900">{proposal.title}</div>
                </td>
                <td className="px-6 py-4 text-sm text-slate-600">{proposal.rfpNumber}</td>
                <td className="px-6 py-4">
                  <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getStatusColor(proposal.status)}`}>
                    {proposal.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-slate-600">{proposal.submittedDate}</td>
                <td className="px-6 py-4 text-sm font-semibold text-slate-900">{proposal.value}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-600 rounded-full"
                        style={{ width: `${proposal.score}%` }}
                      />
                    </div>
                    <span className="text-sm font-semibold">{proposal.score}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <button className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded">
                    <Eye className="w-4 h-4 inline mr-1" />
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
