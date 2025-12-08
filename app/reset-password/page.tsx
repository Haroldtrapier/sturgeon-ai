// app/reset-password/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabaseClient as supabase } from "@/lib/supabaseClient";

export default function ResetPasswordPage() {
  const router = useRouter();
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [sessionReady, setSessionReady] = useState(false);

  // 1) When user lands from email link, Supabase puts tokens in URL hash:
  //    #access_token=...&refresh_token=...
  useEffect(() => {
    const hash = window.location.hash;
    if (!hash) {
      setError("Invalid or expired reset link.");
      return;
    }

    const params = new URLSearchParams(hash.substring(1));
    const accessToken = params.get("access_token");
    const refreshToken = params.get("refresh_token") ?? "";

    if (!accessToken) {
      setError("Invalid or expired reset link.");
      return;
    }

    // 2) Tell Supabase to use this session so we can change the password
    supabase.auth
      .setSession({ access_token: accessToken, refresh_token: refreshToken })
      .then(({ error }) => {
        if (error) {
          console.error("setSession error", error);
          setError("Your reset link is invalid or has expired.");
        } else {
          setSessionReady(true);
        }
      });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!sessionReady) {
      setError("Reset session is not ready. Try the link again from your email.");
      return;
    }

    if (!newPassword || newPassword.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    const { error } = await supabase.auth.updateUser({
      password: newPassword,
    });

    setLoading(false);

    if (error) {
      console.error("updateUser error", error);
      setError(error.message || "Failed to update password.");
      return;
    }

    setSuccess("Password updated successfully. Redirecting to login...");
    setTimeout(() => {
      router.push("/login");
    }, 2000);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4">
      <div className="w-full max-w-md bg-slate-900 border border-slate-700 rounded-xl p-6 shadow-xl">
        <h1 className="text-xl font-semibold text-white mb-2">
          Reset your password
        </h1>
        <p className="text-sm text-slate-300 mb-4">
          Enter a new password for your Sturgeon AI account.
        </p>

        {error && (
          <div className="mb-3 rounded-md bg-red-900/40 border border-red-500 px-3 py-2 text-sm text-red-100">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-3 rounded-md bg-emerald-900/40 border border-emerald-500 px-3 py-2 text-sm text-emerald-100">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <label className="block text-sm text-slate-200 mb-1">
              New password
            </label>
            <input
              type="password"
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              minLength={6}
            />
          </div>

          <div>
            <label className="block text-sm text-slate-200 mb-1">
              Confirm new password
            </label>
            <input
              type="password"
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              minLength={6}
            />
          </div>

          <button
            type="submit"
            disabled={loading || !sessionReady}
            className="w-full rounded-md bg-emerald-500 hover:bg-emerald-400 disabled:bg-slate-600 text-slate-950 font-medium py-2 text-sm transition"
          >
            {loading ? "Updating…" : "Update password"}
          </button>
        </form>

        <p className="mt-4 text-xs text-slate-400">
          If this link doesn't work, request a new reset link from the{" "}
          <a href="/forgot-password" className="text-emerald-400 underline">
            Forgot password
          </a>{" "}
          page.
        </p>
      </div>
    </div>
  );
}
