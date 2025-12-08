"use client";

import { useState } from "react";
import { supabase } from "@/lib/supabaseClient";
import { useRouter } from "next/navigation";

export default function ResetPasswordForm() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function updatePassword() {
    const { error } = await supabase.auth.updateUser({ password });

    if (error) {
      setError(error.message);
      return;
    }

    router.push("/login");
  }

  return (
    <div className="auth-container">
      <h2>Set New Password</h2>

      <input type="password" placeholder="New password" value={password} onChange={e=>setPassword(e.target.value)} />

      {error && <p className="error">{error}</p>}

      <button onClick={updatePassword}>Update Password</button>
    </div>
  );
}
