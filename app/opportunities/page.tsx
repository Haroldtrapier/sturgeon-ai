'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, Calendar, DollarSign, Building2 } from 'lucide-react';

export default function OpportunitiesPage() {
  const router = useRouter();
  const [opportunities, setOpportunities] = useState([]);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const isAuth = localStorage.getItem('isAuthenticated');
    if (!isAuth) {
      router.push('/login');
    } else {
      fetchOpportunities();
    }
  }, [router]);

  const fetchOpportunities = async () => {
    setIsLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://sturgeon-ai-prod.vercel.app';
      const response = await axios.get(`${apiUrl}/api/opportunities/search`, {
        params: { keywords: search || 'AI software', limit: 20 }
      });
      setOpportunities(response.data.opportunities || []);
    } catch (error) {
      console.error('Error fetching opportunities:', error);
      // Mock data for demo
      setOpportunities([
        {
          id: '1',
          title: 'AI-Powered Analytics Platform',
          agency: 'Department of Defense',
          type: 'Contract',
          value: '$2.5M',
          deadline: '2025-12-15',
          description: 'Development of advanced AI analytics platform for military applications'
        },
        {
          id: '2',
          title: 'Cloud Infrastructure Services',
          agency: 'GSA',
          type: 'Contract',
          value: '$1.2M',
          deadline: '2025-11-30',
          description: 'Cloud hosting and infrastructure management services'
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchOpportunities();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-blue-600">Sturgeon AI</h1>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold">Opportunities</h2>
          <p className="mt-2 text-gray-600">Find government contracts and grants</p>
        </div>

        <form onSubmit={handleSearch} className="mb-8">
          <div className="flex gap-4">
            <div className="flex-1">
              <Input
                placeholder="Search opportunities (e.g., 'AI', 'cybersecurity', 'cloud')..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <Button type="submit" disabled={isLoading}>
              <Search className="h-4 w-4 mr-2" />
              {isLoading ? 'Searching...' : 'Search'}
            </Button>
          </div>
        </form>

        <div className="space-y-4">
          {opportunities.length === 0 && !isLoading && (
            <Card>
              <CardContent className="py-12 text-center">
                <p className="text-gray-600">No opportunities found. Try a different search.</p>
              </CardContent>
            </Card>
          )}

          {opportunities.map((opp: any) => (
            <Card key={opp.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle className="text-xl">{opp.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 mb-4">{opp.description}</p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <Building2 className="h-4 w-4 text-gray-500" />
                    <span>{opp.agency}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <DollarSign className="h-4 w-4 text-gray-500" />
                    <span>{opp.value}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-gray-500" />
                    <span>{opp.deadline}</span>
                  </div>
                  <div>
                    <Button size="sm" className="w-full">View Details</Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
