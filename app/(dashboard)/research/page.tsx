'use client';
import { Search, Database } from 'lucide-react';
export default function ContractResearchPage() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-slate-900 mb-2">Contract Research Database</h1>
      <p className="text-slate-600 mb-8">Search and analyze historical federal contracts</p>
      <div className="bg-white rounded-lg shadow p-6">
        <input type="text" placeholder="Search contracts..." className="w-full px-4 py-3 border border-slate-300 rounded-lg" />
      </div>
    </div>
  );
}
