'use client';

import { FormEvent, useState } from 'react';

export default function ForgotPasswordPage() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    setError(null);

    const formData = new FormData(e.currentTarget);
    const email = String(formData.get('email') || '');

    const res = await fetch('/api/auth/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });

    const data = await res.json();

    if (!res.ok) {
      setError(data.error || 'Failed to send reset email');
    } else {
      setMessage(data.message || 'Check your email for a reset link.');
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md bg-white shadow-md rounded-lg p-8 space-y-4"
      >
        <h1 className="text-2xl font-semibold text-slate-900">Reset your password</h1>
        <p className="text-sm text-slate-500">
          Enter the email associated with your Sturgeon AI account.
        </p>

        {error && <p className="text-sm text-red-600">{error}</p>}
        {message && <p className="text-sm text-emerald-600">{message}</p>}

        <div>
          <label className="block text-sm font-medium text-slate-700">Email</label>
          <input
            name="email"
            type="email"
            required
            className="mt-1 w-full border rounded-md px-3 py-2 text-sm"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-md text-sm font-medium disabled:opacity-70"
        >
          {loading ? 'Sending reset link…' : 'Send reset link'}
        </button>

        <p className="text-xs text-slate-500 text-center">
          Remembered your password?{' '}
          <a href="/login" className="text-blue-600 underline">
            Back to login
          </a>
        </p>
      </form>
    </div>
  );
}
