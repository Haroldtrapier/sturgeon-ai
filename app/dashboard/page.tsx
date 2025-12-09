
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [opportunities, setOpportunities] = useState<any[]>([]);
  const [loadingData, setLoadingData] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('supabase-token');
    if (!token) {
      router.push('/login');
      return;
    }

    setUser({ 
      email: 'user@example.com',
      name: 'John Doe',
      role: 'Administrator'
    });
    setLoading(false);

    // Fetch real opportunities from SAM.gov
    fetchOpportunities();
  }, [router]);

  const fetchOpportunities = async () => {
    setLoadingData(true);
    try {
      const response = await fetch('/api/marketplaces/sam?q=technology');
      const data = await response.json();

      if (data.success && data.results) {
        setOpportunities(data.results.slice(0, 5));
      }
    } catch (error) {
      console.error('Error fetching opportunities:', error);
    } finally {
      setLoadingData(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('supabase-token');
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-900">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  const stats = [
    { label: 'Active Opportunities', value: opportunities.length.toString(), change: 'Live Data', positive: true },
    { label: 'SAM.gov Integration', value: 'Active', change: 'Real-time', positive: true },
    { label: 'AI Agents', value: '5', change: 'Working', positive: true },
    { label: 'Data Source', value: 'SAM.gov', change: 'Live', positive: true },
  ];

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <div className="w-64 bg-slate-900 text-white flex flex-col">
        <div className="p-6 border-b border-slate-700">
          <h1 className="text-2xl font-bold">Sturgeon AI</h1>
          <p className="text-slate-400 text-sm mt-1">Gov Contracting</p>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          <button
            onClick={() => setActiveTab('overview')}
            className={`w-full text-left px-4 py-3 rounded-lg transition ${
              activeTab === 'overview' ? 'bg-blue-600' : 'hover:bg-slate-800'
            }`}
          >
            📊 Overview
          </button>

          {/* AI CHAT BUTTON - NEW */}
          <Link
            href="/ai-chat"
            className="block w-full text-left px-4 py-3 rounded-lg transition bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
          >
            <span className="font-semibold">🤖 AI Chat</span>
            <span className="block text-xs text-white/80 mt-1">5 Specialized Agents</span>
          </Link>

          <button
            onClick={() => setActiveTab('opportunities')}
            className={`w-full text-left px-4 py-3 rounded-lg transition ${
              activeTab === 'opportunities' ? 'bg-blue-600' : 'hover:bg-slate-800'
            }`}
          >
            🎯 Opportunities
          </button>
        </nav>

        <div className="p-4 border-t border-slate-700">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center font-bold">
              {user?.name?.charAt(0) || 'U'}
            </div>
            <div className="flex-1 overflow-hidden">
              <p className="font-semibold text-sm truncate">{user?.name || 'User'}</p>
              <p className="text-slate-400 text-xs truncate">{user?.email}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm font-semibold transition"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="bg-white border-b border-slate-200 px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex-1 max-w-2xl">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search contracts, opportunities, agencies..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-4 py-2 pl-10 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <span className="absolute left-3 top-2.5 text-slate-400">🔍</span>
              </div>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-auto p-8">
          {activeTab === 'overview' && (
            <div className="space-y-8">
              <div>
                <h2 className="text-3xl font-bold text-slate-900 mb-2">Dashboard Overview</h2>
                <p className="text-slate-600">Live data from SAM.gov</p>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, i) => (
                  <div key={i} className="bg-white rounded-lg shadow p-6 border border-slate-200">
                    <p className="text-slate-600 text-sm font-medium">{stat.label}</p>
                    <p className="text-3xl font-bold text-slate-900 mt-2">{stat.value}</p>
                    <p className={`text-sm mt-2 ${stat.positive ? 'text-green-600' : 'text-red-600'}`}>
                      {stat.change}
                    </p>
                  </div>
                ))}
              </div>

              {/* Live Opportunities from SAM.gov */}
              <div className="bg-white rounded-lg shadow border border-slate-200">
                <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
                  <h3 className="text-xl font-bold text-slate-900">Live SAM.gov Opportunities</h3>
                  {loadingData && <span className="text-sm text-slate-600">Loading...</span>}
                </div>
                <div className="p-6">
                  {opportunities.length > 0 ? (
                    <div className="space-y-4">
                      {opportunities.map((opp, i) => (
                        <div key={i} className="border border-slate-200 rounded-lg p-4 hover:border-blue-300 transition">
                          <div className="flex justify-between items-start">
                            <div>
                              <h4 className="font-semibold text-slate-900">{opp.title}</h4>
                              <p className="text-slate-600 text-sm mt-1">{opp.agency}</p>
                              <div className="flex gap-2 mt-2 text-xs">
                                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">{opp.source}</span>
                                {opp.status && (
                                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded">{opp.status}</span>
                                )}
                              </div>
                            </div>
                            {opp.link && (
                              <a 
                                href={opp.link} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm"
                              >
                                View
                              </a>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <p className="text-slate-600 mb-4">
                        {loadingData ? 'Fetching live opportunities from SAM.gov...' : 'No opportunities loaded yet'}
                      </p>
                      <button 
                        onClick={fetchOpportunities}
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
                      >
                        Reload Data
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'opportunities' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-slate-900">Search Opportunities</h2>
              <div className="bg-white rounded-lg shadow p-6 border border-slate-200">
                <input
                  type="text"
                  placeholder="Search SAM.gov (e.g., 'cybersecurity', 'IT services')..."
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg mb-4"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      const query = (e.target as HTMLInputElement).value;
                      if (query) {
                        setLoadingData(true);
                        fetch(`/api/marketplaces/sam?q=${encodeURIComponent(query)}`)
                          .then(r => r.json())
                          .then(data => {
                            if (data.success) setOpportunities(data.results || []);
                          })
                          .finally(() => setLoadingData(false));
                      }
                    }
                  }}
                />
                {opportunities.length > 0 && (
                  <div className="space-y-4 mt-6">
                    {opportunities.map((opp, i) => (
                      <div key={i} className="border border-slate-200 rounded-lg p-4">
                        <h4 className="font-semibold">{opp.title}</h4>
                        <p className="text-sm text-slate-600 mt-1">{opp.agency} • {opp.id}</p>
                        {opp.link && (
                          <a href={opp.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 text-sm mt-2 inline-block">
                            View on SAM.gov →
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
