"use client"

import { TransactionsTable } from "@/components/transactions-table"
import { TransactionForm } from "@/components/transaction-form"
import { Receipt, Plus } from "lucide-react"
export default function TransactionsPage() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tight flex items-center gap-3">
            <Receipt className="h-8 w-8 text-[rgb(0,255,178)]" />
            Transactions
          </h1>
          <p className="text-xl text-white/60 mt-2">
            Track and manage all your financial transactions
          </p>
        </div>
        <TransactionForm />
      </div>

      {/* Main Content */}
      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-3">
          <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
            <h2 className="text-2xl font-semibold text-white mb-6">All Transactions</h2>
            <TransactionsTable />
          </div>
        </div>
        
    
      </div>
    </div>
  )
}
