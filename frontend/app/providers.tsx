"use client"

import type { ReactNode } from "react"
import { AuthProvider } from "@/context/auth-context"
import { Analytics } from "@vercel/analytics/next"

export default function Providers({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      {children}
      <Analytics />
    </AuthProvider>
  )
}
