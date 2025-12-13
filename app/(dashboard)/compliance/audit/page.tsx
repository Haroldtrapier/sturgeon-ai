'use client';

import { useState } from 'react';
import { Shield, FileText, Clock, CheckCircle } from 'lucide-react';

export default function AuditTrailPage() {
  const [auditLog] = useState([
    {
      id: '1',
      action: 'Proposal Submitted',
      user: 'John Doe',
      timestamp: '2024-01-15 14:32:10',
      details: 'DOD Cloud Infrastructure RFP Response',
      status: 'Success',
    },
  ]);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-slate-900 mb-2">Compliance Audit Trail</h1>
      <p className="text-slate-600 mb-8">Complete history of compliance-related activities</p>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Timestamp</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Action</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Details</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {auditLog.map((entry) => (
              <tr key={entry.id}>
                <td className="px-6 py-4 text-sm font-mono">{entry.timestamp}</td>
                <td className="px-6 py-4 text-sm font-semibold">{entry.action}</td>
                <td className="px-6 py-4 text-sm">{entry.user}</td>
                <td className="px-6 py-4 text-sm">{entry.details}</td>
                <td className="px-6 py-4">
                  <span className="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">{entry.status}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
