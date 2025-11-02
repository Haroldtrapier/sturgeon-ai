'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

export default function OpportunitiesPage() {
  const router = useRouter();
  const [search, setSearch] = useState('');
  const [opportunities, setOpportunities] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!localStorage.getItem('isAuthenticated')) {
      router.push('/login');
    } else {
      fetchOpportunities();
    }
  }, [router]);

  const fetchOpportunities = async () => {
    setIsLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      const response = await axios.get(`${apiUrl}/api/opportunities/search`, {
        params: { keywords: search || 'AI', limit: 10 }
      });
      setOpportunities(response.data.opportunities || []);
    } catch (error) {
      console.error('Error:', error);
      setOpportunities([
        {
          id: '1',
          title: 'AI Analytics Platform',
          agency: 'DOD',
          value: '$2.5M',
          deadline: '2025-12-15',
          description: 'Advanced AI analytics'
        }
      ]);
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-blue-600">Sturgeon AI</h1>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-6">Opportunities</h2>

        <div className="flex gap-4 mb-6">
          <input
            placeholder="Search opportunities..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 p-2 border rounded"
          />
          <button 
            onClick={fetchOpportunities}
            className="bg-blue-600 text-white px-6 py-2 rounded"
            disabled={isLoading}
          >
            {isLoading ? 'Searching...' : 'Search'}
          </button>
        </div>

        <div className="space-y-4">
          {opportunities.map((opp: any) => (
            <div key={opp.id} className="bg-white p-6 rounded-lg shadow">
              <h3 className="font-bold text-lg">{opp.title}</h3>
              <p className="text-gray-600 mt-2">{opp.description}</p>
              <div className="flex gap-4 mt-4 text-sm">
                <span>{opp.agency}</span>
                <span>{opp.value}</span>
                <span>{opp.deadline}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
