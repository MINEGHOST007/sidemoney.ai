import type React from "react"
import type { Metadata } from "next"
import { DM_Sans } from 'next/font/google'
import "./globals.css"
import Providers from "./providers"
import { Suspense } from "react"

const dmSans = DM_Sans({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-dm-sans',
  weight: ['300', '400', '500', '600', '700', '800']
})

export const metadata: Metadata = {
  title: "sidemoney - AI-Powered Finance Tracker",
  description: "The AI-powered finance tracker that adapts to your lifestyle. Track expenses, set goals, and get intelligent insights.",
  generator: "Next.js",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={dmSans.variable}>
      <body className="font-dm-sans antialiased">
        <Suspense fallback={null}>
          <Providers>{children}</Providers>
        </Suspense>
      </body>
    </html>
  )
}
