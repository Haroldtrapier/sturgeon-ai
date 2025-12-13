'use client';

import { useState } from 'react';
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react';

export default function ComplianceMatrixPage() {
  const [requirements] = useState([
    {
      id: '1',
      section: 'L.3.1',
      requirement: 'Security Clearance Level',
      response: 'Our team holds Top Secret clearances with SCI eligibility',
      status: 'Compliant',
      page: 12,
    },
    {
      id: '2',
      section: 'L.3.2',
      requirement: 'Past Performance - Similar Projects',
      response: 'See Section 3.2 for 5 similar projects delivered',
      status: 'Compliant',
      page: 15,
    },
    {
      id: '3',
      section: 'L.3.3',
      requirement: 'CMMI Level 3 Certification',
      response: 'In progress - Expected Q2 2024',
      status: 'Partial',
      page: 18,
    },
    {
      id: '4',
      section: 'L.3.4',
      requirement: 'ISO 27001 Certification',
      response: 'Not addressed',
      status: 'Missing',
      page: null,
    },
  ]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'Compliant':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'Partial':
        return <AlertCircle className="w-5 h-5 text-yellow-600" />;
      case 'Missing':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Compliant': return 'bg-green-100 text-green-800';
      case 'Partial': return 'bg-yellow-100 text-yellow-800';
      case 'Missing': return 'bg-red-100 text-red-800';
      default: return 'bg-slate-100 text-slate-800';
    }
  };

  const compliantCount = requirements.filter(r => r.status === 'Compliant').length;
  const complianceRate = Math.round((compliantCount / requirements.length) * 100);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Compliance Matrix</h1>
        <p className="text-slate-600">Track RFP requirements and responses</p>
      </div>

      {/* Compliance Score */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-slate-900 mb-2">Overall Compliance</h3>
            <p className="text-3xl font-bold text-slate-900">{complianceRate}%</p>
          </div>
          <div className="flex gap-6">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span className="text-sm font-semibold text-slate-700">Compliant</span>
              </div>
              <p className="text-2xl font-bold text-green-600">{requirements.filter(r => r.status === 'Compliant').length}</p>
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <AlertCircle className="w-5 h-5 text-yellow-600" />
                <span className="text-sm font-semibold text-slate-700">Partial</span>
              </div>
              <p className="text-2xl font-bold text-yellow-600">{requirements.filter(r => r.status === 'Partial').length}</p>
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <XCircle className="w-5 h-5 text-red-600" />
                <span className="text-sm font-semibold text-slate-700">Missing</span>
              </div>
              <p className="text-2xl font-bold text-red-600">{requirements.filter(r => r.status === 'Missing').length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Requirements Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Section</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Requirement</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Response</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Page</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {requirements.map((req) => (
              <tr key={req.id} className="hover:bg-slate-50">
                <td className="px-6 py-4 font-mono text-sm text-slate-900">{req.section}</td>
                <td className="px-6 py-4 text-sm text-slate-900">{req.requirement}</td>
                <td className="px-6 py-4 text-sm text-slate-600">{req.response}</td>
                <td className="px-6 py-4 text-sm text-slate-600">{req.page || '-'}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(req.status)}
                    <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getStatusColor(req.status)}`}>
                      {req.status}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <button className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded">
                    Edit
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
