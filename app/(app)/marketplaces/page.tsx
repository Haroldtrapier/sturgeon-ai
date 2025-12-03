// app/(app)/marketplaces/page.tsx
"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

type Result = {
  id: string;
  title: string;
  agency: string | null;
  status: string;
  source: string;
};

export default function MarketplacesPage() {
  const [marketplace, setMarketplace] = useState<"sam" | "govwin" | "govspend" | "unison">("sam");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);

  async function runSearch() {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(
        `/api/marketplaces/${marketplace}?q=${encodeURIComponent(query)}`
      );
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed");
      setResults(data.results ?? []);
    } catch (e) {
      console.error(e);
      alert("Error searching marketplace");
    } finally {
      setLoading(false);
    }
  }

  async function saveOpp(r: Result) {
    try {
      const res = await fetch("/api/opportunities/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: r.title,
          agency: r.agency,
          source: r.source,
          externalId: r.id,
          status: "watchlist",
          metadata: {},
        }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Failed");
      }
      alert("Saved to opportunities");
    } catch (e) {
      console.error(e);
      alert("Error saving opportunity");
    }
  }

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-2xl font-semibold text-slate-50">
        Marketplaces
      </h1>

      <Card className="p-6">
        <div className="space-y-4">
          <p className="text-sm text-slate-300">
            Unified search across SAM, Unison Marketplace, GovWin, and GovSpend
          </p>

          <div className="grid gap-3 md:grid-cols-3">
            <div className="md:col-span-2">
              <Input
                placeholder="Search keywords (NAICS, PSC, or capabilities)…"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && runSearch()}
              />
            </div>
            <select
              className="flex h-10 w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-50"
              value={marketplace}
              onChange={(e) =>
                setMarketplace(e.target.value as "sam" | "govwin" | "govspend" | "unison")
              }
            >
              <option value="sam">SAM.gov</option>
              <option value="govwin">GovWin</option>
              <option value="govspend">GovSpend</option>
              <option value="unison">Unison</option>
            </select>
          </div>

          <Button 
            onClick={runSearch} 
            disabled={loading || !query.trim()}
          >
            {loading ? "Searching…" : "Search"}
          </Button>
        </div>
      </Card>

      <Card className="p-6">
        <h2 className="mb-4 text-lg font-semibold text-slate-50">
          Results
        </h2>

        {results.length === 0 ? (
          <p className="text-sm text-slate-400">No results yet. Try searching above.</p>
        ) : (
          <div className="space-y-3">
            {results.map((r) => (
              <div
                key={`${r.source}-${r.id}`}
                className="flex items-start justify-between rounded-lg border border-slate-800 bg-slate-900/70 p-4"
              >
                <div className="flex-1">
                  <h3 className="font-medium text-slate-50">{r.title}</h3>
                  <p className="mt-1 text-xs text-slate-400">
                    {r.agency || "No agency"} • {r.source.toUpperCase()} • {r.status}
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => saveOpp(r)}
                  className="ml-3"
                >
                  Save
                </Button>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
