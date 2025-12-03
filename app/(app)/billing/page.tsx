// app/(app)/billing/page.tsx
"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function BillingPage() {
  const [loading, setLoading] = useState<null | "pro" | "enterprise">(null);

  async function startCheckout(plan: "pro" | "enterprise") {
    setLoading(plan);
    try {
      const res = await fetch("/api/subscriptions/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan }),
      });
      const data = await res.json();
      if (!res.ok || !data.url) throw new Error(data.error || "Failed");
      window.location.href = data.url;
    } catch (e) {
      console.error(e);
      alert("Error starting checkout");
      setLoading(null);
    }
  }

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-2xl font-semibold text-slate-50">Billing & Subscriptions</h1>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Free Plan */}
        <Card className="p-6">
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-slate-50">Free</h3>
              <div className="mt-2">
                <span className="text-3xl font-bold text-slate-50">$0</span>
                <span className="text-sm text-slate-400">/month</span>
              </div>
            </div>

            <ul className="space-y-2 text-sm text-slate-300">
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Basic opportunity search</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Save up to 10 opportunities</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Email alerts</span>
              </li>
            </ul>

            <Button variant="outline" className="w-full" disabled>
              Current Plan
            </Button>
          </div>
        </Card>

        {/* Pro Plan */}
        <Card className="relative border-2 border-blue-500 p-6">
          <div className="absolute -top-3 left-1/2 -translate-x-1/2">
            <span className="rounded-full bg-blue-500 px-3 py-1 text-xs font-semibold text-white">
              Most Popular
            </span>
          </div>

          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-slate-50">Pro</h3>
              <div className="mt-2">
                <span className="text-3xl font-bold text-slate-50">$99</span>
                <span className="text-sm text-slate-400">/month</span>
              </div>
            </div>

            <ul className="space-y-2 text-sm text-slate-300">
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Unlimited saved opportunities</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Full proposal builder</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>ContractMatch AI</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Advanced analytics</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Wins tracking</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Priority email support</span>
              </li>
            </ul>

            <Button 
              className="w-full"
              onClick={() => startCheckout("pro")}
              disabled={loading === "pro"}
            >
              {loading === "pro" ? "Redirecting…" : "Upgrade to Pro"}
            </Button>
          </div>
        </Card>

        {/* Enterprise Plan */}
        <Card className="p-6">
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-slate-50">Enterprise</h3>
              <div className="mt-2">
                <span className="text-3xl font-bold text-slate-50">$249</span>
                <span className="text-sm text-slate-400">/month</span>
              </div>
            </div>

            <ul className="space-y-2 text-sm text-slate-300">
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Everything in Pro</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Team collaboration (up to 10 users)</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Custom integrations</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Dedicated account manager</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>24/7 priority support</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✓</span>
                <span>Custom training sessions</span>
              </li>
            </ul>

            <Button
              className="w-full"
              onClick={() => startCheckout("enterprise")}
              disabled={loading === "enterprise"}
            >
              {loading === "enterprise" ? "Redirecting…" : "Upgrade to Enterprise"}
            </Button>
          </div>
        </Card>
      </div>

      {/* FAQ Section */}
      <Card className="p-6">
        <h2 className="mb-4 text-lg font-semibold text-slate-50">
          Frequently Asked Questions
        </h2>

        <div className="space-y-4">
          <div>
            <h3 className="font-medium text-slate-50">Can I cancel anytime?</h3>
            <p className="mt-1 text-sm text-slate-400">
              Yes, you can cancel your subscription at any time. You'll continue to have access until the end of your billing period.
            </p>
          </div>

          <div>
            <h3 className="font-medium text-slate-50">What payment methods do you accept?</h3>
            <p className="mt-1 text-sm text-slate-400">
              We accept all major credit cards (Visa, MasterCard, American Express) through Stripe's secure payment processing.
            </p>
          </div>

          <div>
            <h3 className="font-medium text-slate-50">Can I upgrade or downgrade my plan?</h3>
            <p className="mt-1 text-sm text-slate-400">
              Yes, you can change your plan at any time. When upgrading, you'll be charged a prorated amount. When downgrading, you'll receive credit towards your next billing cycle.
            </p>
          </div>

          <div>
            <h3 className="font-medium text-slate-50">Do you offer refunds?</h3>
            <p className="mt-1 text-sm text-slate-400">
              We offer a 14-day money-back guarantee for first-time subscribers. Contact support if you're not satisfied.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
