"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { Navbar } from "@/components/navbar"
import { useAuth } from "@/context/auth-context"

export default function LoginPage() {
  const { user, loginWithGoogle } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (user) router.replace("/dashboard")
  }, [user, router])

  useEffect(() => {
    // Initialize Google SDK when component mounts
    if (loginWithGoogle) {
      loginWithGoogle()
    }
  }, [loginWithGoogle])

  return (
    <main className="min-h-screen bg-[rgb(8,7,14)]">
      <Navbar />
      <div className="mx-auto max-w-md px-4 py-16 mt-10">
        <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] p-8 shadow-2xl backdrop-blur-sm">
          <div className="text-center mb-6">
            <div className="w-16 h-16 rounded-2xl bg-[rgb(0,255,178)]/10 flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-[rgb(0,255,178)]" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-white">Welcome Back</h1>
            <p className="mt-3 text-white/60 text-lg">
              Sign in to continue managing your finances
            </p>
          </div>

          <div className="mt-8 flex flex-col items-stretch gap-4">
            <div 
              id="google-btn-container" 
              className="w-full min-h-[48px] flex items-center justify-center rounded-xl"
            />
          </div>

          <div className="mt-8 text-center">
            <p className="text-sm text-white/40">
              By continuing you agree to our{" "}
              <a href="#" className="text-[rgb(0,255,178)] hover:text-[rgb(0,255,178)]/80 transition-colors">
                Terms of Service
              </a>{" "}
              and{" "}
              <a href="#" className="text-[rgb(0,255,178)] hover:text-[rgb(0,255,178)]/80 transition-colors">
                Privacy Policy
              </a>
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
