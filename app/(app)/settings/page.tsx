// app/(app)/settings/page.tsx
"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

export default function SettingsPage() {
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    companyName: "",
    naicsCodes: "",
    pscCodes: "",
    cageCode: "",
    duns: "",
    capabilitiesSummary: "",
    certifications: "",
    phone: "",
    website: "",
  });

  function updateField(key: keyof typeof form, value: string) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const res = await fetch("/api/profile");
        const data = await res.json();
        if (res.ok && data.profile) {
          const p = data.profile;
          setForm({
            companyName: p.companyName ?? "",
            naicsCodes: (p.naicsCodes ?? []).join(", "),
            pscCodes: (p.pscCodes ?? []).join(", "),
            cageCode: p.cageCode ?? "",
            duns: p.duns ?? "",
            capabilitiesSummary: p.capabilitiesSummary ?? "",
            certifications: (p.certifications ?? []).join(", "),
            phone: p.phone ?? "",
            website: p.website ?? "",
          });
        }
      } catch (error) {
        console.error("Error loading profile:", error);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  async function handleSave() {
    setSaving(true);
    try {
      const res = await fetch("/api/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          companyName: form.companyName,
          naicsCodes: form.naicsCodes
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean),
          pscCodes: form.pscCodes
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean),
          cageCode: form.cageCode,
          duns: form.duns,
          capabilitiesSummary: form.capabilitiesSummary,
          certifications: form.certifications
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean),
          phone: form.phone,
          website: form.website,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed");
      alert("Profile saved successfully!");
    } catch (e) {
      console.error(e);
      alert("Error saving profile");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-50">
          Company Profile & Settings
        </h1>
        <p className="mt-1 text-sm text-slate-400">
          Manage your company information for better contract matching
        </p>
      </div>

      <Card className="p-6">
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="text-center">
              <div className="mb-2 h-8 w-8 animate-spin rounded-full border-4 border-slate-700 border-t-blue-500"></div>
              <p className="text-sm text-slate-400">Loading profile...</p>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Company Information */}
            <div>
              <h2 className="mb-4 text-lg font-semibold text-slate-50">
                Company Information
              </h2>
              <div className="space-y-4">
                <div>
                  <label className="mb-1 block text-sm font-medium text-slate-300">
                    Company Name
                  </label>
                  <Input
                    placeholder="Enter your company name"
                    value={form.companyName}
                    onChange={(e) => updateField("companyName", e.target.value)}
                  />
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div>
                    <label className="mb-1 block text-sm font-medium text-slate-300">
                      Phone Number
                    </label>
                    <Input
                      placeholder="(555) 123-4567"
                      value={form.phone}
                      onChange={(e) => updateField("phone", e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="mb-1 block text-sm font-medium text-slate-300">
                      Website
                    </label>
                    <Input
                      placeholder="https://yourcompany.com"
                      value={form.website}
                      onChange={(e) => updateField("website", e.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Government Identifiers */}
            <div>
              <h2 className="mb-4 text-lg font-semibold text-slate-50">
                Government Identifiers
              </h2>
              <div className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div>
                    <label className="mb-1 block text-sm font-medium text-slate-300">
                      CAGE Code
                    </label>
                    <Input
                      placeholder="5-character CAGE code"
                      value={form.cageCode}
                      onChange={(e) => updateField("cageCode", e.target.value)}
                      maxLength={5}
                    />
                    <p className="mt-1 text-xs text-slate-500">
                      Commercial and Government Entity Code
                    </p>
                  </div>
                  <div>
                    <label className="mb-1 block text-sm font-medium text-slate-300">
                      DUNS Number
                    </label>
                    <Input
                      placeholder="9-digit DUNS number"
                      value={form.duns}
                      onChange={(e) => updateField("duns", e.target.value)}
                      maxLength={9}
                    />
                    <p className="mt-1 text-xs text-slate-500">
                      Data Universal Numbering System (legacy)
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Classification Codes */}
            <div>
              <h2 className="mb-4 text-lg font-semibold text-slate-50">
                Classification Codes
              </h2>
              <div className="space-y-4">
                <div>
                  <label className="mb-1 block text-sm font-medium text-slate-300">
                    NAICS Codes
                  </label>
                  <Input
                    placeholder="e.g., 541512, 541519, 541611"
                    value={form.naicsCodes}
                    onChange={(e) => updateField("naicsCodes", e.target.value)}
                  />
                  <p className="mt-1 text-xs text-slate-500">
                    North American Industry Classification System (comma separated)
                  </p>
                </div>

                <div>
                  <label className="mb-1 block text-sm font-medium text-slate-300">
                    PSC Codes
                  </label>
                  <Input
                    placeholder="e.g., D301, D302, R425"
                    value={form.pscCodes}
                    onChange={(e) => updateField("pscCodes", e.target.value)}
                  />
                  <p className="mt-1 text-xs text-slate-500">
                    Product Service Codes (comma separated)
                  </p>
                </div>
              </div>
            </div>

            {/* Capabilities & Certifications */}
            <div>
              <h2 className="mb-4 text-lg font-semibold text-slate-50">
                Capabilities & Certifications
              </h2>
              <div className="space-y-4">
                <div>
                  <label className="mb-1 block text-sm font-medium text-slate-300">
                    Capabilities Summary
                  </label>
                  <Textarea
                    rows={4}
                    placeholder="Describe your company's core capabilities, expertise, and what makes you competitive..."
                    value={form.capabilitiesSummary}
                    onChange={(e) =>
                      updateField("capabilitiesSummary", e.target.value)
                    }
                  />
                  <p className="mt-1 text-xs text-slate-500">
                    This helps our AI match you with relevant opportunities
                  </p>
                </div>

                <div>
                  <label className="mb-1 block text-sm font-medium text-slate-300">
                    Certifications
                  </label>
                  <Input
                    placeholder="e.g., SDVOSB, HUBZone, 8(a), WOSB"
                    value={form.certifications}
                    onChange={(e) => updateField("certifications", e.target.value)}
                  />
                  <p className="mt-1 text-xs text-slate-500">
                    Small business certifications (comma separated)
                  </p>
                </div>
              </div>
            </div>

            {/* Save Button */}
            <div className="flex items-center justify-end border-t border-slate-800 pt-6">
              <Button 
                onClick={handleSave} 
                disabled={saving}
                size="lg"
              >
                {saving ? "Saving…" : "Save Profile"}
              </Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
