'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function AnalyticsPage() {
  const router = useRouter();

  useEffect(() => {
    if (!localStorage.getItem('isAuthenticated')) {
      router.push('/login');
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-blue-600">Sturgeon AI</h1>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-6">Analytics</h2>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-6 rounded-lg text-center">
            <p className="text-3xl font-bold text-blue-600">101</p>
            <p className="text-sm text-gray-600">Total Proposals</p>
          </div>
          <div className="bg-green-50 p-6 rounded-lg text-center">
            <p className="text-3xl font-bold text-green-600">38</p>
            <p className="text-sm text-gray-600">Wins</p>
          </div>
          <div className="bg-purple-50 p-6 rounded-lg text-center">
            <p className="text-3xl font-bold text-purple-600">38%</p>
            <p className="text-sm text-gray-600">Win Rate</p>
          </div>
          <div className="bg-orange-50 p-6 rounded-lg text-center">
            <p className="text-3xl font-bold text-orange-600">$12.5M</p>
            <p className="text-sm text-gray-600">Total Value</p>
          </div>
        </div>
      </div>
    </div>
  );
}
