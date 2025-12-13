'use client';

import { useState } from 'react';
import { Database, FileText, TrendingUp, BarChart } from 'lucide-react';

export default function FPDSPage() {
  const [contracts] = useState([
    {
      piid: 'W52P1J24D0015',
      title: 'IT Infrastructure Support Services',
      agency: 'Department of Defense',
      contractor: 'Tech Solutions Inc.',
      value: '$45M',
      type: 'IDIQ',
      date: '2024-01-15',
      naics: '541512',
    },
    {
      piid: 'HSHQDC24C00123',
      title: 'Cybersecurity Services',
      agency: 'Department of Homeland Security',
      contractor: 'SecureIT Corp',
      value: '$12.5M',
      type: 'Firm Fixed Price',
      date: '2024-01-10',
      naics: '541519',
    },
  ]);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">
          Federal Procurement Data System (FPDS)
        </h1>
        <p className="text-slate-600">Comprehensive federal contracting data and awards</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <Database className="w-8 h-8 text-blue-600" />
            <h3 className="text-2xl font-bold">2.8M</h3>
          </div>
          <p className="text-slate-600 text-sm">Contract Actions (FY24)</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <FileText className="w-8 h-8 text-green-600" />
            <h3 className="text-2xl font-bold">$698B</h3>
          </div>
          <p className="text-slate-600 text-sm">Total Obligations</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="w-8 h-8 text-purple-600" />
            <h3 className="text-2xl font-bold">+6.2%</h3>
          </div>
          <p className="text-slate-600 text-sm">YoY Growth</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3 mb-2">
            <BarChart className="w-8 h-8 text-orange-600" />
            <h3 className="text-2xl font-bold">125K</h3>
          </div>
          <p className="text-slate-600 text-sm">Active Contractors</p>
        </div>
      </div>

      {/* Advanced Search */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Advanced Search</h3>
        <div className="grid grid-cols-3 gap-4 mb-4">
          <input
            type="text"
            placeholder="PIID or Contract Number"
            className="px-4 py-2 border border-slate-300 rounded-lg"
          />
          <select className="px-4 py-2 border border-slate-300 rounded-lg">
            <option>All Agencies</option>
            <option>DOD</option>
            <option>DHS</option>
            <option>GSA</option>
            <option>VA</option>
          </select>
          <input
            type="text"
            placeholder="NAICS Code"
            className="px-4 py-2 border border-slate-300 rounded-lg"
          />
        </div>
        <div className="grid grid-cols-3 gap-4 mb-4">
          <select className="px-4 py-2 border border-slate-300 rounded-lg">
            <option>All Contract Types</option>
            <option>IDIQ</option>
            <option>FFP</option>
            <option>T&M</option>
            <option>CPFF</option>
          </select>
          <input
            type="date"
            className="px-4 py-2 border border-slate-300 rounded-lg"
          />
          <input
            type="date"
            className="px-4 py-2 border border-slate-300 rounded-lg"
          />
        </div>
        <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
          Search FPDS
        </button>
      </div>

      {/* Recent Awards */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200">
          <h3 className="text-lg font-semibold text-slate-900">Recent Contract Awards</h3>
        </div>
        <table className="w-full">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">PIID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Title</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Agency</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Contractor</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Value</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {contracts.map((contract) => (
              <tr key={contract.piid} className="hover:bg-slate-50">
                <td className="px-6 py-4 text-sm font-mono text-blue-600">{contract.piid}</td>
                <td className="px-6 py-4 text-sm font-semibold text-slate-900">{contract.title}</td>
                <td className="px-6 py-4 text-sm text-slate-600">{contract.agency}</td>
                <td className="px-6 py-4 text-sm text-slate-600">{contract.contractor}</td>
                <td className="px-6 py-4 text-sm font-semibold text-slate-900">{contract.value}</td>
                <td className="px-6 py-4">
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full">
                    {contract.type}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-slate-600">{contract.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
