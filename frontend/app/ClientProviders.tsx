"use client"

import type React from "react"

import { Analytics } from "@vercel/analytics/next"
import "./globals.css"
import Providers from "./providers" // <CHANGE> use client-side providers wrapper
import { Suspense } from "react"

export default function ClientProviders({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <>
      <Suspense fallback={null}>
        <Providers>
          {children}
        </Providers>
      </Suspense>
      <Analytics />
    </>
  )
}
