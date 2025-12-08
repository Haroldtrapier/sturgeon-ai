'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.currentTarget);
    const email = String(formData.get('email') || '');
    const password = String(formData.get('password') || '');

    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      setError(data.error || 'Login failed');
      setLoading(false);
      return;
    }

    router.push('/dashboard'); // or whatever your main app route is
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md bg-white shadow-md rounded-lg p-8 space-y-4"
      >
        <h1 className="text-2xl font-semibold text-slate-900">Sturgeon AI</h1>
        <p className="text-sm text-slate-500">Welcome back!</p>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <div>
          <label className="block text-sm font-medium text-slate-700">Email</label>
          <input
            name="email"
            type="email"
            required
            className="mt-1 w-full border rounded-md px-3 py-2 text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700">Password</label>
          <input
            name="password"
            type="password"
            required
            className="mt-1 w-full border rounded-md px-3 py-2 text-sm"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-md text-sm font-medium disabled:opacity-70"
        >
          {loading ? 'Signing in…' : 'Sign In'}
        </button>

        <div className="flex justify-between text-xs text-slate-500">
          <a href="/forgot-password" className="text-blue-600 underline">
            Forgot password?
          </a>
          <a href="/signup" className="text-blue-600 underline">
            Create account
          </a>
        </div>
      </form>
    </div>
  );
}