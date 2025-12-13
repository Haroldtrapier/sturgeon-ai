'use client';

import { useState } from 'react';
import { FileText, Download, Copy, Star } from 'lucide-react';

export default function ProposalTemplatesPage() {
  const [templates] = useState([
    {
      id: '1',
      name: 'Standard IT Services Proposal',
      description: 'Comprehensive template for IT services contracts',
      category: 'IT Services',
      sections: 12,
      pages: 45,
      rating: 4.8,
      uses: 156,
    },
    {
      id: '2',
      name: 'Cybersecurity Assessment RFP Response',
      description: 'Specialized template for cybersecurity proposals',
      category: 'Cybersecurity',
      sections: 10,
      pages: 38,
      rating: 4.9,
      uses: 203,
    },
    {
      id: '3',
      name: 'Cloud Migration Services',
      description: 'Template for cloud infrastructure and migration projects',
      category: 'Cloud Services',
      sections: 14,
      pages: 52,
      rating: 4.7,
      uses: 89,
    },
  ]);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Proposal Templates</h1>
        <p className="text-slate-600">Pre-built templates to accelerate your proposal creation</p>
      </div>

      {/* Categories */}
      <div className="flex gap-3 mb-6">
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg">All Templates</button>
        <button className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50">IT Services</button>
        <button className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50">Cybersecurity</button>
        <button className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50">Cloud</button>
        <button className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50">Consulting</button>
      </div>

      {/* Templates Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {templates.map((template) => (
          <div key={template.id} className="bg-white rounded-lg shadow p-6 border border-slate-200 hover:shadow-lg transition">
            <div className="flex items-start justify-between mb-4">
              <FileText className="w-12 h-12 text-blue-600" />
              <div className="flex items-center gap-1">
                <Star className="w-4 h-4 text-yellow-500 fill-current" />
                <span className="text-sm font-semibold">{template.rating}</span>
              </div>
            </div>

            <h3 className="text-lg font-semibold text-slate-900 mb-2">{template.name}</h3>
            <p className="text-sm text-slate-600 mb-4">{template.description}</p>

            <div className="flex gap-4 text-sm text-slate-600 mb-4">
              <div>{template.sections} sections</div>
              <div>{template.pages} pages</div>
              <div>{template.uses} uses</div>
            </div>

            <div className="flex gap-2">
              <button className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold flex items-center justify-center gap-2">
                <Copy className="w-4 h-4" />
                Use Template
              </button>
              <button className="px-3 py-2 border border-slate-300 rounded-lg hover:bg-slate-50">
                <Download className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
