"use client"
import type React from "react"
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react"
import { apiGet, apiPost } from "@/lib/api"

type User = {
  id: string
  email: string
  name: string
  avatar_url?: string
  monthly_income?: number
  preferred_spending_days?: string[]
  daily_budget_multiplier?: number
  current_amount?: number
  created_at?: string
  updated_at?: string
}

type AuthContextValue = {
  user: User | null
  token: string | null
  isLoading: boolean
  loginWithGoogle: () => void
  logout: () => void
  refreshMe: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

declare global {
  interface Window {
    google?: any
  }
}

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null)
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Load token from localStorage
  useEffect(() => {
    const t = localStorage.getItem("access_token")
    if (t) setToken(t)
    setIsLoading(false)
  }, [])

  const refreshMe = useCallback(async () => {
    if (!token) return
    try {
      const me = await apiGet<User>("/auth/me")
      setUser(me)
    } catch (e) {
      console.error("[v0] /auth/me failed:", e)
      // Token might be invalid/expired
    }
  }, [token])

  useEffect(() => {
    if (token) {
      refreshMe()
    } else {
      setUser(null)
    }
  }, [token, refreshMe])

  // Google Identity Services init on login page render when needed
  const loginWithGoogle = useCallback(() => {
    if (!GOOGLE_CLIENT_ID) {
      alert("Missing NEXT_PUBLIC_GOOGLE_CLIENT_ID")
      return
    }
    // Load script if not present
    const existing = document.getElementById("google-identity")
    const ensureInit = () => {
      if (!window.google) return
      try {
        window.google.accounts.id.initialize({
          client_id: GOOGLE_CLIENT_ID,
          callback: async (response: { credential: string }) => {
            try {
              // Send id_token to backend to exchange for access token
              const data = await apiPost<{
                access_token: string
                token_type: string
                expires_in: number
                user_id: string
              }>("/auth/google", { id_token: response.credential }, false)
              localStorage.setItem("access_token", data.access_token)
              setToken(data.access_token)
              await refreshMe()
            } catch (e: any) {
              alert(`Login failed: ${e?.message || "Unknown error"}`)
            }
          },
        })
        window.google.accounts.id.prompt() // One Tap if available
        // Also render a button container if present
        const btn = document.getElementById("google-btn-container")
        if (btn) {
          window.google.accounts.id.renderButton(btn, {
            theme: "filled_black",
            size: "large",
            type: "standard",
            shape: "rectangular",
            text: "continue_with",
            logo_alignment: "left",
            width: "100%"
          })
        }
      } catch (e) {
        console.error("[v0] Google init error", e)
      }
    }

    if (!existing) {
      const script = document.createElement("script")
      script.id = "google-identity"
      script.src = "https://accounts.google.com/gsi/client"
      script.async = true
      script.defer = true
      script.onload = ensureInit
      document.head.appendChild(script)
    } else {
      ensureInit()
    }
  }, [])

  const logout = useCallback(async () => {
    try {
      await apiPost<{ message: string }>("/auth/logout", {}, true)
    } catch {
      // ignore
    } finally {
      localStorage.removeItem("access_token")
      setToken(null)
      setUser(null)
    }
  }, [])

  const value = useMemo(
    () => ({ user, token, isLoading, loginWithGoogle, logout, refreshMe }),
    [user, token, isLoading, loginWithGoogle, logout, refreshMe],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error("useAuth must be used within AuthProvider")
  return ctx
}
