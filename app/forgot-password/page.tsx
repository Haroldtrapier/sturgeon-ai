"use client";

import { useState } from "react";
import { supabase } from "@/lib/supabaseClient";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleReset() {
    setError("");
    setMessage("");

    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${process.env.NEXT_PUBLIC_SITE_URL}/reset-password`
    });

    if (error) {
      setError(error.message);
      return;
    }

    setMessage("Password reset link has been sent to your email.");
  }

  return (
    <div className="auth-container">
      <h2>Reset Your Password</h2>

      <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />

      {error && <p className="error">{error}</p>}
      {message && <p className="success">{message}</p>}

      <button onClick={handleReset}>Send Reset Link</button>
    </div>
  );
}
