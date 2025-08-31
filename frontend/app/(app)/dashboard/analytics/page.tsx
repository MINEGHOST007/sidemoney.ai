"use client"

import { AnalyticsCharts } from "@/components/analytics-charts"
import { TrendingUp, BarChart3, PieChart, LineChart, Loader2, AlertCircle } from "lucide-react"
import useSWR from "swr"
import { apiGet } from "@/lib/api"
import { formatCurrency, formatCompactCurrency } from "@/lib/utils"

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

type MonthlyReport = {
  year: number
  month: number
  total_income: number
  total_expenses: number
  net_change: number
  category_breakdown: Record<string, number>
  insights: string[]
}

type CategoryBreakdown = {
  start_date: string
  end_date: string
  total_expenses: number
  category_totals: Record<string, number>
  category_percentages: Record<string, number>
  transaction_count: number
  insights: string[]
}

export default function AnalyticsPage() {
  const { data: report, isLoading: reportLoading, error: reportError } = useSWR<DailyReport>("/analytics/daily-report", apiGet)
  const { data: monthlyReport, isLoading: monthlyLoading } = useSWR<MonthlyReport>("/analytics/monthly-report", apiGet)
  const { data: categoryData, isLoading: categoryLoading } = useSWR<CategoryBreakdown>("/analytics/category-breakdown", apiGet)

  // Calculate insights from data
  const topCategory = categoryData ? 
    Object.entries(categoryData.category_percentages || {})
      .sort(([,a], [,b]) => b - a)[0] : null
  
  const savingsRate = monthlyReport ? 
    monthlyReport.total_income > 0 ? 
      ((monthlyReport.total_income - monthlyReport.total_expenses) / monthlyReport.total_income * 100) : 0 
    : 0

  const monthlyTrend = monthlyReport?.net_change || 0

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tight flex items-center gap-3">
            <TrendingUp className="h-8 w-8 text-[rgb(0,255,178)]" />
            Analytics
          </h1>
          <p className="text-xl text-white/60 mt-2">
            Deep insights into your financial patterns
          </p>
        </div>
      </div>

      {/* Analytics Overview */}
      {reportError ? (
        <div className="flex items-center gap-2 p-6 bg-white/5 border border-white/10 rounded-2xl text-white/70">
          <AlertCircle className="h-6 w-6" />
          <span>Failed to load analytics data. Please try again.</span>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <BarChart3 className="h-5 w-5 text-[rgb(0,255,178)]" />
                  <span className="text-white/60 text-sm font-medium">Monthly Trend</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {monthlyLoading ? "..." : monthlyTrend >= 0 ? `+${formatCompactCurrency(monthlyTrend)}` : formatCompactCurrency(monthlyTrend)}
                </div>
                <div className={`text-sm ${monthlyTrend >= 0 ? 'text-[rgb(0,255,178)]' : 'text-white/70'}`}>
                  {monthlyTrend >= 0 ? 'Surplus this month' : 'Deficit this month'}
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <PieChart className="h-5 w-5 text-[rgb(0,255,178)]" />
                  <span className="text-white/60 text-sm font-medium">Top Category</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {categoryLoading ? "..." : (topCategory?.[0]?.replace(/_/g, ' ') || "None")}
                </div>
                <div className="text-sm text-white/60">
                  {topCategory ? `${Math.round(topCategory[1])}% of expenses` : 'No data'}
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <LineChart className="h-5 w-5 text-[rgb(0,255,178)]" />
                  <span className="text-white/60 text-sm font-medium">Daily Budget</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {reportLoading ? "..." : formatCompactCurrency(report?.daily_budget || 0)}
                </div>
                <div className="text-sm text-white/60">Budget allocation</div>
              </div>
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <TrendingUp className="h-5 w-5 text-[rgb(0,255,178)]" />
                  <span className="text-white/60 text-sm font-medium">Savings Rate</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {monthlyLoading ? "..." : `${Math.round(savingsRate)}%`}
                </div>
                <div className={`text-sm ${savingsRate >= 20 ? 'text-[rgb(0,255,178)]' : savingsRate >= 10 ? 'text-yellow-400' : 'text-white/70'}`}>
                  {savingsRate >= 20 ? 'Excellent' : savingsRate >= 10 ? 'Good' : 'Needs improvement'}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Detailed Charts */}
      <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
        <h2 className="text-2xl font-semibold text-white mb-6">Detailed Analytics</h2>
        {reportLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-[rgb(0,255,178)]" />
            <span className="ml-2 text-white/60">Loading charts...</span>
          </div>
        ) : (
          <AnalyticsCharts report={report} />
        )}
      </div>

      {/* AI Insights */}
      {report?.insights && report.insights.length > 0 && (
        <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
          <h2 className="text-2xl font-semibold text-white mb-6">AI Insights</h2>
          <div className="space-y-4">
            {report.insights.map((insight, index) => (
              <div key={index} className="bg-[rgba(255,255,255,0.05)] rounded-xl p-4 border border-white/5">
                <p className="text-white/80 leading-relaxed">{insight}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
