"use client";
import { useState } from 'react';
import { supabaseClient as supabase } from '@/lib/supabaseClient';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    const origin =
      typeof window !== 'undefined'
        ? window.location.origin
        : 'https://sturgeon-ai.vercel.app';

    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${origin}/reset-password`,
    });

    if (error) setMessage(`Failed to send reset email: ${error.message}`);
    else setMessage('Check your email for a reset link.');
    setLoading(false);
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: '2rem auto' }}>
      <h1>Forgot Password</h1>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@example.com"
        required
        style={{ width: '100%', padding: 8, marginBottom: 16 }}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Sending...' : 'Send Reset Link'}
      </button>
      {message && <p>{message}</p>}
    </form>
  );
}
