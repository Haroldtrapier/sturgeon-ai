'use client';

import { useState } from 'react';
import { Lightbulb, Plus } from 'lucide-react';

export default function WinThemesPage() {
  const [themes] = useState([
    {
      id: '1',
      title: 'Proven Track Record in Federal Cloud Migration',
      description: 'Emphasize our 15+ successful cloud migrations for DOD agencies',
      sections: ['Executive Summary', 'Past Performance', 'Technical Approach'],
      strength: 'High',
    },
    {
      id: '2',
      title: 'Security-First Architecture',
      description: 'Highlight our zero-breach record and FedRAMP High authorization',
      sections: ['Security Approach', 'Risk Management', 'Technical Solution'],
      strength: 'Very High',
    },
    {
      id: '3',
      title: 'Cost Optimization Through AI',
      description: 'Showcase 30% average cost savings using AI-driven optimization',
      sections: ['Cost Proposal', 'Value Proposition', 'ROI Analysis'],
      strength: 'Medium',
    },
  ]);

  return (
    <div className="p-8">
      <div className="mb-8">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 mb-2">Win Themes</h1>
            <p className="text-slate-600">Create compelling narratives for your proposals</p>
          </div>
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2 font-semibold">
            <Plus className="w-5 h-5" />
            Add Win Theme
          </button>
        </div>
      </div>

      {/* Win Themes */}
      <div className="space-y-6">
        {themes.map((theme) => (
          <div key={theme.id} className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-600">
            <div className="flex items-start gap-4">
              <Lightbulb className="w-8 h-8 text-blue-600 flex-shrink-0 mt-1" />
              <div className="flex-1">
                <div className="flex items-start justify-between gap-4 mb-3">
                  <div>
                    <h3 className="text-xl font-semibold text-slate-900 mb-2">{theme.title}</h3>
                    <p className="text-slate-600">{theme.description}</p>
                  </div>
                  <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                    theme.strength === 'Very High' ? 'bg-green-100 text-green-800' :
                    theme.strength === 'High' ? 'bg-blue-100 text-blue-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {theme.strength} Strength
                  </span>
                </div>

                <div className="mb-4">
                  <p className="text-sm font-semibold text-slate-700 mb-2">Applies to sections:</p>
                  <div className="flex gap-2">
                    {theme.sections.map((section, idx) => (
                      <span key={idx} className="px-3 py-1 bg-slate-100 text-slate-700 text-sm rounded">
                        {section}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex gap-2">
                  <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm">
                    Edit Theme
                  </button>
                  <button className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 text-sm">
                    Apply to Proposal
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
