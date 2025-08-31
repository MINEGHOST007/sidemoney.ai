"use client"

import { GoalsList } from "@/components/goals-list"
import { Target, Plus, TrendingUp, Calendar, DollarSign } from "lucide-react"
import { Button } from "@/components/ui/button"
import useSWR from "swr"
import { apiGet } from "@/lib/api"
import { formatCurrency, formatCompactCurrency } from "@/lib/utils"

type GoalProgress = {
  goals: {
    id: string
    title: string
    target_amount: number
    deadline: string
    current_amount: number
    progress_percentage: number
    days_remaining: number
    amount_needed: number
    daily_savings_needed: number
  }[]
  total_goals: number
  overall_progress: number
}

type GoalsResponse = {
  goals: {
    id: string
    title: string
    target_amount: number
    deadline: string
    created_at?: string
    updated_at?: string
  }[]
  total: number
}

export default function GoalsPage() {
  const { data: goalsData, isLoading: goalsLoading } = useSWR<GoalsResponse>("/goals", apiGet)
  const { data: progressData, isLoading: progressLoading } = useSWR<GoalProgress>("/analytics/goal-progress", apiGet)

  const totalSaved = progressData?.goals?.reduce((sum, goal) => sum + goal.current_amount, 0) ?? 0
  const averageProgress = progressData?.overall_progress ?? 0
  const activeGoalsCount = goalsData?.total ?? 0

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tight flex items-center gap-3">
            <Target className="h-8 w-8 text-[rgb(0,255,178)]" />
            Financial Goals
          </h1>
          <p className="text-xl text-white/60 mt-2">
            Set and track your financial milestones
          </p>
        </div>
      </div>

      {/* Goals Overview */}
      <div className="grid gap-6 md:grid-cols-3">
        <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="text-white/60 text-sm font-medium mb-2">Active Goals</div>
              <div className="text-3xl font-bold text-white mb-2">
                {goalsLoading ? "..." : activeGoalsCount}
              </div>
            </div>
            <div className="w-12 h-12 rounded-xl bg-[rgb(0,255,178)]/10 flex items-center justify-center">
              <Target className="h-6 w-6 text-[rgb(0,255,178)]" />
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="text-white/60 text-sm font-medium mb-2">Total Saved</div>
              <div className="text-3xl font-bold text-[rgb(0,255,178)] mb-2">
                {progressLoading ? "..." : formatCompactCurrency(totalSaved)}
              </div>
            </div>
            <div className="w-12 h-12 rounded-xl bg-[rgb(0,255,178)]/10 flex items-center justify-center">
              <DollarSign className="h-6 w-6 text-[rgb(0,255,178)]" />
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="text-white/60 text-sm font-medium mb-2">Average Progress</div>
              <div className="text-3xl font-bold text-white mb-2">
                {progressLoading ? "..." : `${Math.round(averageProgress)}%`}
              </div>
            </div>
            <div className="w-12 h-12 rounded-xl bg-[rgb(0,255,178)]/10 flex items-center justify-center">
              <TrendingUp className="h-6 w-6 text-[rgb(0,255,178)]" />
            </div>
          </div>
        </div>
      </div>

      {/* Goal Progress Cards */}
      {progressData?.goals && progressData.goals.length > 0 && (
        <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center">
              <TrendingUp className="h-5 w-5 text-[rgb(0,255,178)]" />
            </div>
            <h2 className="text-2xl font-semibold text-white">Goal Progress Tracker</h2>
          </div>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {progressData.goals.map((goal) => {
              const progressColor = goal.progress_percentage >= 75 
                ? "text-green-400" 
                : goal.progress_percentage >= 50 
                ? "text-[rgb(0,255,178)]" 
                : goal.progress_percentage >= 25 
                ? "text-yellow-400" 
                : "text-white/70"
              
              const progressBgColor = goal.progress_percentage >= 75 
                ? "bg-green-400" 
                : goal.progress_percentage >= 50 
                ? "bg-[rgb(0,255,178)]" 
                : goal.progress_percentage >= 25 
                ? "bg-yellow-400" 
                : "bg-white/50"

              return (
                <div key={goal.id} className="bg-white/5 rounded-xl border border-white/10 p-5 hover:bg-white/10 transition-all duration-300 group">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="font-semibold text-white mb-2 text-lg">{goal.title}</h3>
                      <div className="text-sm text-white/60 mb-3">
                        Target: {formatCurrency(goal.target_amount)}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={`text-2xl font-bold ${progressColor}`}>
                        {Math.round(goal.progress_percentage)}%
                      </div>
                      <div className="text-xs text-white/60">Complete</div>
                    </div>
                  </div>
                  
                  {/* Progress Bar */}
                  <div className="w-full bg-white/10 rounded-full h-3 mb-4">
                    <div 
                      className={`${progressBgColor} h-3 rounded-full transition-all duration-500 ease-out`}
                      style={{ width: `${Math.min(goal.progress_percentage, 100)}%` }}
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="bg-white/5 rounded-lg p-3">
                      <div className="text-white/60 text-xs font-medium mb-1">Need to Save</div>
                      <div className="text-white font-semibold">
                        {formatCurrency(Math.max(0, goal.amount_needed))}
                      </div>
                    </div>
                    <div className="bg-white/5 rounded-lg p-3">
                      <div className="text-white/60 text-xs font-medium mb-1">Days Left</div>
                      <div className={`font-semibold ${goal.days_remaining <= 30 ? 'text-yellow-400' : 'text-white'}`}>
                        {Math.max(0, goal.days_remaining)} days
                      </div>
                    </div>
                    <div className="col-span-2 bg-[rgb(0,255,178)]/10 rounded-lg p-3 border border-[rgb(0,255,178)]/20">
                      <div className="text-white/60 text-xs font-medium mb-1">Daily Savings Needed</div>
                      <div className="text-[rgb(0,255,178)] font-bold text-lg">
                        {formatCurrency(Math.max(0, goal.daily_savings_needed))}
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Goals Management */}
      <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center">
            <Target className="h-5 w-5 text-[rgb(0,255,178)]" />
          </div>
          <h2 className="text-2xl font-semibold text-white">Manage Your Goals</h2>
        </div>
        <GoalsList />
      </div>
    </div>
  )
}
