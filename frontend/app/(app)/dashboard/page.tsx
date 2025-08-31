"use client"

import useSWR from "swr"
import { apiGet, apiPost } from "@/lib/api"
import { formatCurrency, formatCompactCurrency } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { TransactionsTable } from "@/components/transactions-table"
import { TransactionForm } from "@/components/transaction-form"
import { GoalsList } from "@/components/goals-list"
import { AnalyticsCharts } from "@/components/analytics-charts"
import { OcrUpload } from "@/components/ocr-upload"
import { 
  TrendingUp, 
  DollarSign, 
  Target as TargetIcon, 
  Calendar,
  Plus,
  BarChart3,
  Sparkles,
  Camera
} from "lucide-react"

type DailyBudget = {
  daily_budget: number
  daily_budget_with_multiplier: number
  monthly_income: number
  active_goals_count: number
  days_until_earliest_goal: number
  money_needed_total: number
  money_needed_per_day: number
  current_amount: number
}

type DailyReport = {
  date: string
  total_income: number
  total_expenses: number
  net_change: number
  daily_budget: number
  budget_remaining: number
  category_breakdown: Record<string, number>
  transaction_count: number
  insights: string[]
}

export default function DashboardPage() {
  const { data: budget } = useSWR<DailyBudget>("/analytics/daily-budget", apiGet)
  const { data: report } = useSWR<DailyReport>("/analytics/daily-report", apiGet)

  // Get current time for greeting
  const currentHour = new Date().getHours()
  const greeting = currentHour < 12 ? "Good morning" : currentHour < 18 ? "Good afternoon" : "Good evening"

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tight">
            {greeting}
          </h1>
          <p className="text-xl text-white/60 mt-2">
            Here's what's happening with your finances today
          </p>
        </div>

        
          <TransactionForm />
       
      </div>

      {/* Stats Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Today's Budget"
          value={budget ? formatCurrency(budget.daily_budget_with_multiplier || 0) : "—"}
          icon={DollarSign}
          trend="+12% from yesterday"
          trendUp={true}
        />
        <StatsCard
          title="Monthly Income"
          value={budget ? formatCurrency(budget.monthly_income || 0) : "—"}
          icon={TrendingUp}
          trend="Steady income flow"
          trendUp={true}
        />
        <StatsCard
          title="Active Goals"
          value={budget?.active_goals_count?.toString() ?? "—"}
          icon={TargetIcon}
          trend={budget?.days_until_earliest_goal ? `${budget.days_until_earliest_goal} days to next goal` : "No active goals"}
          trendUp={false}
        />
        <StatsCard
          title="Remaining Today"
          value={report ? formatCurrency(report.budget_remaining || 0) : "—"}
          icon={Calendar}
          trend={report?.budget_remaining && report.budget_remaining > 0 ? "On track" : "Over budget"}
          trendUp={report?.budget_remaining ? report.budget_remaining > 0 : false}
        />
      </div>

      {/* Analytics Overview */}
      <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center">
            <BarChart3 className="h-5 w-5 text-[rgb(0,255,178)]" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Financial Overview</h2>
            <p className="text-white/60">Your spending patterns and insights</p>
          </div>
        </div>
        <AnalyticsCharts report={report} />
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="transactions" className="space-y-6">
        <div className="border-b border-white/10">
          <TabsList className="bg-transparent border-0 p-0 h-auto space-x-8">
            <TabsTrigger 
              value="transactions" 
              className="bg-transparent border-0 text-white/60 hover:text-white data-[state=active]:text-[rgb(0,255,178)] data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-[rgb(0,255,178)] rounded-none px-0 py-4 text-lg font-medium transition-colors"
            >
              Transactions
            </TabsTrigger>
            <TabsTrigger 
              value="goals" 
              className="bg-transparent border-0 text-white/60 hover:text-white data-[state=active]:text-[rgb(0,255,178)] data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-[rgb(0,255,178)] rounded-none px-0 py-4 text-lg font-medium transition-colors"
            >
              Goals
            </TabsTrigger>
            <TabsTrigger 
              value="ocr" 
              className="bg-transparent border-0 text-white/60 hover:text-white data-[state=active]:text-[rgb(0,255,178)] data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-[rgb(0,255,178)] rounded-none px-0 py-4 text-lg font-medium transition-colors"
            >
              Receipt Scanner
            </TabsTrigger>
          </TabsList>
        </div>

        <TabsContent value="transactions" className="space-y-6 mt-8">
          <div className="grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
                <h3 className="text-xl font-semibold text-white mb-4">Recent Transactions</h3>
                <TransactionsTable />
              </div>
            </div>
            <div className="lg:col-span-1">
              <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6 h-fit">
                <h3 className="text-xl font-semibold text-white mb-4">Add Transaction</h3>
                <TransactionForm />
              </div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="goals" className="mt-8">
          <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
            <h3 className="text-xl font-semibold text-white mb-4">Financial Goals</h3>
            <GoalsList />
          </div>
        </TabsContent>

        <TabsContent value="ocr" className="mt-8">
          <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-[rgb(0,255,178)]/10 flex items-center justify-center">
                <Camera className="h-6 w-6 text-[rgb(0,255,178)]" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">Receipt Scanner</h3>
                <p className="text-white/60">Upload receipt photos for automatic transaction extraction</p>
              </div>
            </div>
            <OcrUpload />
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

// Stats Card Component
function StatsCard({ 
  title, 
  value, 
  icon: Icon, 
  trend, 
  trendUp 
}: { 
  title: string
  value: string
  icon: any
  trend: string
  trendUp: boolean
}) {
  return (
    <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6 hover:border-[rgb(0,255,178)]/30 transition-all duration-300 group">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-white/60 text-sm font-medium mb-2">{title}</p>
          <p className="text-3xl font-bold text-white mb-3">{value}</p>
          <div className="flex items-center gap-2">
            <span className={`text-sm ${trendUp ? 'text-[rgb(0,255,178)]' : 'text-white/40'}`}>
              {trend}
            </span>
          </div>
        </div>
        <div className="w-12 h-12 rounded-xl bg-[rgb(0,255,178)]/10 flex items-center justify-center group-hover:bg-[rgb(0,255,178)]/20 transition-colors">
          <Icon className="h-6 w-6 text-[rgb(0,255,178)]" />
        </div>
      </div>
    </div>
  )
}
