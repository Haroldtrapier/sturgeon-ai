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
  }, [router]);

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
    { label: 'Active Contracts', value: '24', change: '+12%', positive: true },
    { label: 'Total Revenue', value: '$2.4M', change: '+8%', positive: true },
    { label: 'Opportunities', value: '156', change: '+23%', positive: true },
    { label: 'Win Rate', value: '68%', change: '-3%', positive: false },
  ];

  const contracts = [
    { id: 'C-001', agency: 'Department of Defense', value: '$450K', status: 'Active', date: '2024-01-15' },
    { id: 'C-002', agency: 'NASA', value: '$850K', status: 'Active', date: '2024-02-20' },
    { id: 'C-003', agency: 'DHS', value: '$320K', status: 'Pending', date: '2024-03-10' },
    { id: 'C-004', agency: 'VA', value: '$180K', status: 'Active', date: '2024-03-25' },
  ];

  const opportunities = [
    { id: 'O-101', title: 'Cybersecurity Infrastructure', agency: 'DoD', value: '$1.2M', deadline: '2024-12-15' },
    { id: 'O-102', title: 'Cloud Migration Services', agency: 'GSA', value: '$900K', deadline: '2024-12-20' },
    { id: 'O-103', title: 'AI/ML Development', agency: 'NASA', value: '$2.5M', deadline: '2025-01-10' },
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
            onClick={() => setActiveTab('contracts')}
            className={`w-full text-left px-4 py-3 rounded-lg transition ${
              activeTab === 'contracts' ? 'bg-blue-600' : 'hover:bg-slate-800'
            }`}
          >
            📝 Contracts
          </button>
          <button
            onClick={() => setActiveTab('opportunities')}
            className={`w-full text-left px-4 py-3 rounded-lg transition ${
              activeTab === 'opportunities' ? 'bg-blue-600' : 'hover:bg-slate-800'
            }`}
          >
            🎯 Opportunities
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`w-full text-left px-4 py-3 rounded-lg transition ${
              activeTab === 'analytics' ? 'bg-blue-600' : 'hover:bg-slate-800'
            }`}
          >
            📈 Analytics
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`w-full text-left px-4 py-3 rounded-lg transition ${
              activeTab === 'settings' ? 'bg-blue-600' : 'hover:bg-slate-800'
            }`}
          >
            ⚙️ Settings
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
            <div className="flex items-center gap-4 ml-6">
              <button className="p-2 hover:bg-slate-100 rounded-lg">🔔</button>
              <button className="p-2 hover:bg-slate-100 rounded-lg">💬</button>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-auto p-8">
          {activeTab === 'overview' && (
            <div className="space-y-8">
              <div>
                <h2 className="text-3xl font-bold text-slate-900 mb-2">Dashboard Overview</h2>
                <p className="text-slate-600">Welcome back! Here's what's happening with your contracts.</p>
              </div>

              {/* AI Chat CTA */}
              <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg shadow-lg p-8 text-white">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-2xl font-bold mb-2">🤖 Try Our AI Agents</h3>
                    <p className="text-white/90 mb-4">
                      Get instant help with contract analysis, proposal writing, compliance checking, and more!
                    </p>
                    <Link
                      href="/ai-chat"
                      className="inline-block px-6 py-3 bg-white text-purple-600 font-bold rounded-lg hover:bg-slate-100 transition"
                    >
                      Start Chatting →
                    </Link>
                  </div>
                  <div className="text-6xl">💬</div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, i) => (
                  <div key={i} className="bg-white rounded-lg shadow p-6 border border-slate-200">
                    <p className="text-slate-600 text-sm font-medium">{stat.label}</p>
                    <p className="text-3xl font-bold text-slate-900 mt-2">{stat.value}</p>
                    <p className={`text-sm mt-2 ${stat.positive ? 'text-green-600' : 'text-red-600'}`}>
                      {stat.change} from last month
                    </p>
                  </div>
                ))}
              </div>

              <div className="bg-white rounded-lg shadow border border-slate-200">
                <div className="px-6 py-4 border-b border-slate-200">
                  <h3 className="text-xl font-bold text-slate-900">Recent Contracts</h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-slate-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">ID</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Agency</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Value</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Status</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Date</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200">
                      {contracts.map((contract) => (
                        <tr key={contract.id} className="hover:bg-slate-50">
                          <td className="px-6 py-4 text-sm font-medium text-slate-900">{contract.id}</td>
                          <td className="px-6 py-4 text-sm text-slate-600">{contract.agency}</td>
                          <td className="px-6 py-4 text-sm text-slate-900 font-semibold">{contract.value}</td>
                          <td className="px-6 py-4">
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                              contract.status === 'Active' 
                                ? 'bg-green-100 text-green-800' 
                                : 'bg-yellow-100 text-yellow-800'
                            }`}>
                              {contract.status}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-sm text-slate-600">{contract.date}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'contracts' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-slate-900">All Contracts</h2>
              <div className="bg-white rounded-lg shadow border border-slate-200 overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">ID</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Agency</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Value</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Date</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200">
                    {contracts.map((contract) => (
                      <tr key={contract.id} className="hover:bg-slate-50">
                        <td className="px-6 py-4 text-sm font-medium text-slate-900">{contract.id}</td>
                        <td className="px-6 py-4 text-sm text-slate-600">{contract.agency}</td>
                        <td className="px-6 py-4 text-sm text-slate-900 font-semibold">{contract.value}</td>
                        <td className="px-6 py-4">
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            contract.status === 'Active' 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {contract.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-slate-600">{contract.date}</td>
                        <td className="px-6 py-4 text-sm">
                          <button className="text-blue-600 hover:text-blue-800 font-medium">View</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'opportunities' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-slate-900">Open Opportunities</h2>
              <div className="grid gap-4">
                {opportunities.map((opp) => (
                  <div key={opp.id} className="bg-white rounded-lg shadow p-6 border border-slate-200 hover:border-blue-300 transition">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-slate-900 mb-2">{opp.title}</h3>
                        <p className="text-slate-600 mb-3">{opp.agency} • {opp.id}</p>
                        <div className="flex gap-4 text-sm">
                          <span className="font-semibold text-green-600">{opp.value}</span>
                          <span className="text-slate-500">Deadline: {opp.deadline}</span>
                        </div>
                      </div>
                      <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
                        Apply
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'analytics' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-slate-900">Analytics</h2>
              <div className="bg-white rounded-lg shadow p-8 border border-slate-200">
                <p className="text-slate-600">📊 Advanced analytics and reporting coming soon...</p>
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-slate-900">Settings</h2>
              <div className="bg-white rounded-lg shadow p-6 border border-slate-200 space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">Profile Information</h3>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">Name</label>
                      <input type="text" value={user?.name} className="w-full px-3 py-2 border border-slate-300 rounded-lg" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                      <input type="email" value={user?.email} className="w-full px-3 py-2 border border-slate-300 rounded-lg" disabled />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">Role</label>
                      <input type="text" value={user?.role} className="w-full px-3 py-2 border border-slate-300 rounded-lg" disabled />
                    </div>
                  </div>
                </div>
                <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
                  Save Changes
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
