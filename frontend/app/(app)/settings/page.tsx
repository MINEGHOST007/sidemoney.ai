"use client"

import type React from "react"

import useSWR from "swr"
import { apiGet, apiPut } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useState, useEffect } from "react"

type Profile = {
  id: string
  email: string
  name: string
  monthly_income?: number
  daily_budget_multiplier?: number
  current_amount?: number
  preferred_spending_days?: string[]
  created_at?: string
}

const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

export default function SettingsPage() {
  const { data, mutate } = useSWR<Profile>("/user/profile", apiGet)
  const [name, setName] = useState("")
  const [monthlyIncome, setMonthlyIncome] = useState("")
  const [multiplier, setMultiplier] = useState("")
  const [currentAmount, setCurrentAmount] = useState("")
  const [preferredDays, setPreferredDays] = useState<string[]>([])

  useEffect(() => {
    if (data) {
      setName(data.name || "")
      setMonthlyIncome(String(data.monthly_income ?? ""))
      setMultiplier(String(data.daily_budget_multiplier ?? ""))
      setCurrentAmount(String(data.current_amount ?? ""))
      setPreferredDays(data.preferred_spending_days || [])
    }
  }, [data])

  async function onSave(e: React.FormEvent) {
    e.preventDefault()
    await apiPut("/user/profile", {
      name: name || undefined,
      monthly_income: monthlyIncome ? Number(monthlyIncome) : undefined,
      daily_budget_multiplier: multiplier ? Number(multiplier) : undefined,
      current_amount: currentAmount ? Number(currentAmount) : undefined,
      preferred_spending_days: preferredDays,
    })
    mutate()
    alert("Profile updated")
  }

  function toggleDay(d: string) {
    setPreferredDays((prev) => (prev.includes(d) ? prev.filter((x) => x !== d) : [...prev, d]))
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>
      <form className="grid gap-4 max-w-xl rounded-lg border bg-white p-4" onSubmit={onSave}>
        <div className="grid gap-1">
          <Label>Name</Label>
          <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Your name" />
        </div>
        <div className="grid gap-1">
          <Label>Monthly Income</Label>
          <Input type="number" step="0.01" value={monthlyIncome} onChange={(e) => setMonthlyIncome(e.target.value)} />
        </div>
        <div className="grid gap-1">
          <Label>Daily Budget Multiplier</Label>
          <Input type="number" step="0.1" value={multiplier} onChange={(e) => setMultiplier(e.target.value)} />
        </div>
        <div className="grid gap-1">
          <Label>Current Amount</Label>
          <Input type="number" step="0.01" value={currentAmount} onChange={(e) => setCurrentAmount(e.target.value)} />
        </div>
        <div className="grid gap-2">
          <Label>Preferred Spending Days</Label>
          <div className="flex flex-wrap gap-2">
            {days.map((d) => (
              <button
                key={d}
                type="button"
                onClick={() => toggleDay(d)}
                className={`px-3 py-1 rounded-full border ${preferredDays.includes(d) ? "bg-blue-600 text-white border-blue-600" : "bg-white text-gray-700"}`}
              >
                {d}
              </button>
            ))}
          </div>
        </div>
        <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
          Save
        </Button>
      </form>
    </div>
  )
}
