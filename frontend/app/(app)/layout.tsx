"use client"

import type React from "react"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/context/auth-context"
import { Navbar } from "@/components/navbar"

function Guard({ children }: { children: React.ReactNode }) {
  const { token, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !token) {
      router.replace("/login")
    }
  }, [token, isLoading, router])

  if (!token) {
    return (
      <div className="min-h-screen bg-[rgb(8,7,14)] text-white">
        <Navbar />
        <div className="mx-auto max-w-7xl px-4 py-24">
          <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] p-8 text-center">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-[rgb(0,255,178)] border-r-transparent"></div>
            <p className="mt-4 text-white/70">Checking authentication...</p>
          </div>
        </div>
      </div>
    )
  }
  return <>{children}</>
}

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[rgb(8,7,14)] text-white">
      <Navbar />
      {/* main content */}
      <main className="mx-auto max-w-7xl px-4 py-8 pt-24">
        <Guard>{children}</Guard>
      </main>
    </div>
  )
}
