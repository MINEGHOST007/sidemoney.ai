"use client"

import type React from "react"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"
import { AuthProvider } from "@/context/auth-context" // add provider
import { Suspense } from "react" // import Suspense
import { useSearchParams } from "next/navigation" // import useSearchParams

export default function ClientLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  const searchParams = useSearchParams() // useSearchParams hook

  return (
    <html lang="en">
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable}`}>
        <Suspense fallback={<div>Loading...</div>}>
          {" "}
          {/* Suspense boundary */}
          <AuthProvider>
            {children}
            <Analytics />
          </AuthProvider>
        </Suspense>
      </body>
    </html>
  )
}
