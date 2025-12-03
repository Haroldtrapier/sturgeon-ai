// app/(app)/billing/success/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function BillingSuccessPage() {
  const searchParams = useSearchParams();
  const plan = searchParams.get("plan");
  const isDev = searchParams.get("dev");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate verification delay
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1500);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-slate-700 border-t-blue-500"></div>
          <p className="text-slate-400">Verifying your subscription...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center p-6">
      <Card className="max-w-md p-8 text-center">
        <div className="mb-4 flex justify-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-green-500/10">
            <svg
              className="h-8 w-8 text-green-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
        </div>

        <h1 className="mb-2 text-2xl font-bold text-slate-50">
          Welcome to {plan === "enterprise" ? "Enterprise" : "Pro"}!
        </h1>

        <p className="mb-6 text-slate-400">
          Your subscription is now active. You have full access to all {plan === "enterprise" ? "Enterprise" : "Pro"} features.
        </p>

        {isDev && (
          <div className="mb-6 rounded-lg bg-yellow-500/10 p-4">
            <p className="text-sm text-yellow-500">
              <strong>Development Mode:</strong> This is a test subscription. No actual payment was processed.
            </p>
          </div>
        )}

        <div className="space-y-3">
          <Link href="/dashboard">
            <Button className="w-full">
              Go to Dashboard
            </Button>
          </Link>

          <Link href="/marketplaces">
            <Button variant="outline" className="w-full">
              Explore Marketplaces
            </Button>
          </Link>
        </div>

        <div className="mt-6 border-t border-slate-800 pt-6">
          <p className="text-sm text-slate-400">
            Need help getting started?{" "}
            <a href="/docs" className="text-blue-400 hover:underline">
              View documentation
            </a>
          </p>
        </div>
      </Card>
    </div>
  );
}
