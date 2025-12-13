'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import Sidebar from '@/components/layout/Sidebar';
import Header from '@/components/layout/Header';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('supabase-token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Fetch user data
    setUser({
      name: 'John Doe',
      email: 'user@example.com',
    });
    setLoading(false);
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('supabase-token');
    router.push('/login');
  };

  const handleSearch = (query: string) => {
    // Implement global search
    router.push(`/search?q=${encodeURIComponent(query)}`);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-900">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-slate-50">
      <Sidebar user={user} onLogout={handleLogout} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header onSearch={handleSearch} />
        <main className="flex-1 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
