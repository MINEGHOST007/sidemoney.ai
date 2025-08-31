"use client"

import type React from "react"

import useSWR from "swr"
import useSWRMutation from "swr/mutation"
import { apiDelete, apiGet, apiPost } from "@/lib/api"
import { formatCurrency } from "@/lib/utils"
import { useCacheInvalidation } from "@/hooks/use-cache-invalidation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"
import { useState } from "react"
import { Trash2, Loader2, AlertCircle, Target, Calendar, DollarSign, Plus } from "lucide-react"

type Goal = {
  id: string
  title: string
  target_amount: number
  deadline: string
  created_at?: string
  updated_at?: string
}

type GoalsResponse = {
  goals: Goal[]
  total: number
}

export function GoalsList() {
  const { data, mutate: mutateGoals, isLoading, error } = useSWR<GoalsResponse>("/goals", apiGet)
  const [title, setTitle] = useState("")
  const [amount, setAmount] = useState("")
  const [deadline, setDeadline] = useState("")
  const [isDeleting, setIsDeleting] = useState<string | null>(null)
  const { toast } = useToast()
  const { invalidateGoalData } = useCacheInvalidation()

  const { trigger, isMutating } = useSWRMutation("/goals", async (_key, { arg }: { arg: any }) => {
    return apiPost("/goals", arg)
  })

  async function createGoal(e: React.FormEvent) {
    e.preventDefault()
    const amt = Number.parseFloat(amount)
    if (!title || title.length < 1) {
      toast({
        title: "Error",
        description: "Goal title is required",
      })
      return
    }
    if (!amt || amt <= 0) {
      toast({
        title: "Error", 
        description: "Target amount must be greater than 0",
      })
      return
    }
    if (!deadline) {
      toast({
        title: "Error",
        description: "Deadline is required",
      })
      return
    }
    const d = new Date(deadline)
    if (d.getTime() < Date.now()) {
      toast({
        title: "Error",
        description: "Deadline must be in the future",
      })
      return
    }
    
    try {
      await trigger({ title, target_amount: amt, deadline })
      setTitle("")
      setAmount("")
      setDeadline("")
      
      // Invalidate all dependent caches to trigger refetch
      await invalidateGoalData()
      
      toast({
        title: "Success!",
        description: "Goal created successfully",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to create goal. Please try again.",
      })
    }
  }

  async function del(id: string) {
    setIsDeleting(id)
    try {
      await apiDelete(`/goals/${id}`)
      
      // Invalidate all dependent caches to trigger refetch
      await invalidateGoalData()
      
      toast({
        title: "Success!",
        description: "Goal deleted successfully",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete goal. Please try again.",
      })
    } finally {
      setIsDeleting(null)
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-5">
      {/* Create Goal Form */}
      <div className="lg:col-span-2">
        <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6 h-fit">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center">
              <Plus className="h-5 w-5 text-[rgb(0,255,178)]" />
            </div>
            <h3 className="text-xl font-semibold text-white">Create New Goal</h3>
          </div>
          <form className="space-y-4" onSubmit={createGoal}>
            <div className="space-y-2">
              <Label className="text-white/90 font-medium flex items-center gap-2">
                <Target className="h-4 w-4" />
                Goal Title
              </Label>
              <Input 
                value={title} 
                onChange={(e) => setTitle(e.target.value)} 
                placeholder="Emergency Fund, New Car, Vacation..." 
                className="bg-white/5 border-white/20 text-white placeholder:text-white/50 hover:bg-white/10 focus:ring-[rgb(0,255,178)]/50 focus:border-[rgb(0,255,178)]/50 transition-colors"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-white/90 font-medium flex items-center gap-2">
                <DollarSign className="h-4 w-4" />
                Target Amount (₹)
              </Label>
              <Input
                type="number"
                step="0.01"
                min="1"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="50000.00"
                className="bg-white/5 border-white/20 text-white placeholder:text-white/50 hover:bg-white/10 focus:ring-[rgb(0,255,178)]/50 focus:border-[rgb(0,255,178)]/50 transition-colors"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-white/90 font-medium flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                Deadline
              </Label>
              <Input 
                type="date" 
                value={deadline} 
                onChange={(e) => setDeadline(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
                className="bg-white/5 border-white/20 text-white hover:bg-white/10 focus:ring-[rgb(0,255,178)]/50 focus:border-[rgb(0,255,178)]/50 transition-colors"
              />
            </div>
            <Button 
              type="submit" 
              disabled={isMutating} 
              className="w-full bg-[rgb(0,255,178)] text-black hover:bg-[rgb(0,255,178)]/90 font-semibold py-3 rounded-xl shadow-lg shadow-[rgb(0,255,178)]/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-all duration-300"
            >
              {isMutating ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Creating Goal...
                </>
              ) : (
                <>
                  <Plus className="h-4 w-4" />
                  Create Goal
                </>
              )}
            </Button>
          </form>
        </div>
      </div>

      {/* Goals List */}
      <div className="lg:col-span-3">
        <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center">
              <Target className="h-5 w-5 text-[rgb(0,255,178)]" />
            </div>
            <h3 className="text-xl font-semibold text-white">Your Goals</h3>
            {data?.total && (
              <div className="ml-auto">
                <span className="px-3 py-1 rounded-full bg-[rgb(0,255,178)]/10 text-[rgb(0,255,178)] text-sm font-medium">
                  {data.total} {data.total === 1 ? 'Goal' : 'Goals'}
                </span>
              </div>
            )}
          </div>
          
          {error && (
            <div className="flex items-center gap-3 p-4 bg-white/5 border border-white/20 rounded-xl text-white/70 mb-4">
              <AlertCircle className="h-5 w-5 flex-shrink-0 text-[rgb(0,255,178)]" />
              <div>
                <div className="font-medium text-white">Failed to load goals</div>
                <div className="text-sm text-white/60">Please check your connection and try again.</div>
              </div>
            </div>
          )}
          
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-[rgb(0,255,178)] mb-3" />
              <span className="text-white/60">Loading your goals...</span>
            </div>
          ) : data?.goals && data.goals.length > 0 ? (
            <div className="space-y-4">
              {data.goals.map((g) => {
                const daysLeft = Math.max(0, Math.ceil((new Date(g.deadline).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)))
                const isOverdue = new Date(g.deadline) < new Date()
                
                return (
                  <div key={g.id} className="bg-white/5 rounded-xl border border-white/10 p-5 hover:bg-white/10 transition-all duration-300 group">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <Target className="h-4 w-4 text-[rgb(0,255,178)]" />
                          <h4 className="font-semibold text-white text-lg">{g.title}</h4>
                        </div>
                        <div className="space-y-2">
                          <div className="flex items-center gap-4 text-sm">
                            <div className="flex items-center gap-1">
                              <DollarSign className="h-3 w-3 text-[rgb(0,255,178)]" />
                              <span className="text-white/60">Target:</span>
                              <span className="font-semibold text-[rgb(0,255,178)]">
                                {formatCurrency(Number(g.target_amount))}
                              </span>
                            </div>
                          </div>
                          <div className="flex items-center gap-4 text-sm">
                            <div className="flex items-center gap-1">
                              <Calendar className="h-3 w-3 text-white/60" />
                              <span className="text-white/60">Due:</span>
                              <span className={`font-medium ${isOverdue ? 'text-yellow-400' : daysLeft <= 30 ? 'text-yellow-400' : 'text-white'}`}>
                                {new Date(g.deadline).toLocaleDateString('en-IN', { 
                                  day: 'numeric', 
                                  month: 'short', 
                                  year: 'numeric' 
                                })}
                              </span>
                              {!isOverdue && (
                                <span className="text-white/60">
                                  ({daysLeft} {daysLeft === 1 ? 'day' : 'days'} left)
                                </span>
                              )}
                              {isOverdue && (
                                <span className="text-yellow-400 text-xs">
                                  (Overdue)
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                      <Button 
                        variant="ghost" 
                        size="sm"
                        onClick={() => del(g.id)}
                        disabled={isDeleting === g.id}
                        className="text-white/60 hover:text-white hover:bg-white/10 transition-colors opacity-0 group-hover:opacity-100"
                      >
                        {isDeleting === g.id ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          <Trash2 className="h-4 w-4" />
                        )}
                      </Button>
                    </div>
                  </div>
                )
              })}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4">
                <Target className="h-8 w-8 text-white/40" />
              </div>
              <div className="text-white/60 mb-2 text-lg font-medium">No goals yet</div>
              <div className="text-sm text-white/40 max-w-sm mx-auto">
                Create your first financial goal to start tracking your progress towards achieving your dreams.
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
