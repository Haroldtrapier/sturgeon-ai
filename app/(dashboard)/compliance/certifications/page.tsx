'use client';

import { useState } from 'react';
import { Award, Calendar } from 'lucide-react';

export default function CertificationsTrackerPage() {
  const [certifications] = useState([
    { id: '1', name: 'ISO 27001:2013', status: 'Active', expiryDate: '2026-06-15', authority: 'BSI Group' },
    { id: '2', name: 'FedRAMP High', status: 'Active', expiryDate: '2026-09-01', authority: 'FedRAMP PMO' },
  ]);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-slate-900 mb-2">Certifications Tracker</h1>
      <p className="text-slate-600 mb-8">Manage required certifications and credentials</p>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Certification</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Authority</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Expiry</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {certifications.map((cert) => (
              <tr key={cert.id}>
                <td className="px-6 py-4 font-semibold">{cert.name}</td>
                <td className="px-6 py-4 text-sm">{cert.authority}</td>
                <td className="px-6 py-4 text-sm">{cert.expiryDate}</td>
                <td className="px-6 py-4">
                  <span className="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">{cert.status}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
