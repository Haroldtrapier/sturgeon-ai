'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useLocalStorage } from '@/lib/useClientStorage';

export default function Dashboard() {
  const router = useRouter();
  const [token, setToken, isClient] = useLocalStorage('supabase-token');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (isClient && !token) {
      router.push('/login');
    }
  }, [isClient, token, router]);

  if (!mounted) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <button onClick={() => {
        setToken(null);
        router.push('/login');
      }}>
        Logout
      </button>
    </div>
  );
}
