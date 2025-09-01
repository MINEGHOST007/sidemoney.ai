"use client";

import type React from "react";

import useSWR from "swr";
import { apiGet, apiPut } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { useState, useEffect } from "react";
import {
  User,
  DollarSign,
  Calendar,
  UserCircle,
  Save,
  Check,
} from "lucide-react";

type Profile = {
  id: string;
  email: string;
  name: string;
  monthly_income?: number;
  daily_budget_multiplier?: number;
  current_amount?: number;
  preferred_spending_days?: string[];
  created_at?: string;
};

const days = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];

export default function ProfilePage() {
  const { data, mutate } = useSWR<Profile>("/user/profile", apiGet);
  const [name, setName] = useState("");
  const [monthlyIncome, setMonthlyIncome] = useState("");
  const [multiplier, setMultiplier] = useState("");
  const [currentAmount, setCurrentAmount] = useState("");
  const [preferredDays, setPreferredDays] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    if (data) {
      setName(data.name || "");
      setMonthlyIncome(String(data.monthly_income ?? ""));
      setMultiplier(String(data.daily_budget_multiplier ?? ""));
      setCurrentAmount(String(data.current_amount ?? ""));
      setPreferredDays(data.preferred_spending_days || []);
    }
  }, [data]);

  async function onSave(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);
    setShowSuccess(false);
    try {
      await apiPut("/user/profile", {
        name: name || undefined,
        monthly_income: monthlyIncome ? Number(monthlyIncome) : undefined,
        daily_budget_multiplier: multiplier ? Number(multiplier) : undefined,
        current_amount: currentAmount ? Number(currentAmount) : undefined,
        preferred_spending_days: preferredDays,
      });
      mutate();
      // Show success feedback using React state
      setShowSuccess(true);
      setTimeout(() => {
        setShowSuccess(false);
      }, 3000);
    } finally {
      setIsLoading(false);
    }
  }

  function toggleDay(d: string) {
    setPreferredDays((prev) =>
      prev.includes(d) ? prev.filter((x) => x !== d) : [...prev, d]
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tight">
            Profile
          </h1>
          <p className="text-xl text-white/60 mt-2">
            Manage your account and financial preferences
          </p>
        </div>
        <div className="w-12 h-12 rounded-xl bg-[rgb(0,255,178)]/10 flex items-center justify-center">
          <UserCircle className="h-6 w-6 text-[rgb(0,255,178)]" />
        </div>
      </div>

      <form onSubmit={onSave} className="space-y-6">
        {/* Personal Information */}
        <Card className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] border border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-white">
              <div className="w-10 h-10 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center">
                <User className="h-5 w-5 text-[rgb(0,255,178)]" />
              </div>
              Personal Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label className="text-white font-medium">Full Name</Label>
              <Input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your full name"
                className="bg-white/5 border-white/20 text-white placeholder:text-white/40 focus:border-[rgb(0,255,178)]/50 focus:ring-[rgb(0,255,178)]/20"
              />
            </div>
            <div className="grid gap-2">
              <Label className="text-white font-medium">Email Address</Label>
              <Input
                value={data?.email || ""}
                disabled
                className="bg-white/5 border-white/10 text-white/60 cursor-not-allowed"
              />
              <p className="text-sm text-white/40">Email cannot be changed</p>
            </div>
          </CardContent>
        </Card>

        {/* Financial Settings */}
        <Card className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] border border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-white">
              <div className="w-10 h-10 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center">
                <DollarSign className="h-5 w-5 text-[rgb(0,255,178)]" />
              </div>
              Financial Settings
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label className="text-white font-medium">Monthly Income</Label>
              <Input
                type="number"
                step="0.01"
                value={monthlyIncome}
                onChange={(e) => setMonthlyIncome(e.target.value)}
                placeholder="Enter your monthly income"
                className="bg-white/5 border-white/20 text-white placeholder:text-white/40 focus:border-[rgb(0,255,178)]/50 focus:ring-[rgb(0,255,178)]/20"
              />
            </div>
            <div className="grid gap-2">
              <Label className="text-white font-medium">
                Spending Day Multiple
              </Label>
              <Input
                type="number"
                step="0.1"
                value={multiplier}
                onChange={(e) => setMultiplier(e.target.value)}
                placeholder="e.g., 1.2 for 20% extra budget"
                className="bg-white/5 border-white/20 text-white placeholder:text-white/40 focus:border-[rgb(0,255,178)]/50 focus:ring-[rgb(0,255,178)]/20"
              />
              <p className="text-sm text-white/60">
                Higher budget on preferred spending days, lower on others to
                balance monthly total
              </p>
            </div>
            <div className="grid gap-2">
              <Label className="text-white font-medium">Current Amount</Label>
              <Input
                type="number"
                step="0.01"
                value={currentAmount}
                onChange={(e) => setCurrentAmount(e.target.value)}
                placeholder="Enter your current balance"
                className="bg-white/5 border-white/20 text-white placeholder:text-white/40 focus:border-[rgb(0,255,178)]/50 focus:ring-[rgb(0,255,178)]/20"
              />
            </div>
          </CardContent>
        </Card>

        {/* Spending Preferences */}
        <Card className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] border border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-white">
              <div className="w-10 h-10 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center">
                <Calendar className="h-5 w-5 text-[rgb(0,255,178)]" />
              </div>
              Spending Preferences
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-3">
              <Label className="text-white font-medium">
                Preferred Spending Days
              </Label>
              <p className="text-sm text-white/60">
                Select the days when you typically make purchases
              </p>
              <div className="flex flex-wrap gap-2">
                {days.map((d) => (
                  <button
                    key={d}
                    type="button"
                    onClick={() => toggleDay(d)}
                    className={`px-4 py-2 rounded-lg border transition-all duration-200 ${
                      preferredDays.includes(d)
                        ? "bg-[rgb(0,255,178)]/20 text-[rgb(0,255,178)] border-[rgb(0,255,178)]/50 shadow-lg shadow-[rgb(0,255,178)]/10"
                        : "bg-white/5 text-white/70 border-white/20 hover:bg-white/10 hover:text-white"
                    }`}
                  >
                    {d}
                  </button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Save Button */}
        <div className="flex justify-end pt-4">
          <Button
            type="submit"
            disabled={isLoading}
            className="bg-[rgb(0,255,178)] text-black hover:bg-[rgb(0,255,178)]/90 font-semibold px-8 py-3 rounded-xl transition-all duration-200 shadow-lg shadow-[rgb(0,255,178)]/20 disabled:opacity-50"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-black/20 border-t-black mr-2" />
                Saving...
              </>
            ) : showSuccess ? (
              <>
                <Check className="h-4 w-4 mr-2" />
                Saved!
              </>
            ) : (
              <>
                <Save className="h-4 w-4 mr-2" />
                Save Changes
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  );
}
