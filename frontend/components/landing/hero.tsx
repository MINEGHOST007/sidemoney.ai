"use client"

import Image from "next/image"
import DashboardPreview from "./dashboard-preview"
import { Button } from "@/components/ui/button"

export default function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        {/* Accent bars using the fixed palette without gradients */}
        <div className="absolute -top-16 -left-16 h-48 w-48 rotate-12 bg-primary/15 blur-2xl animate-float" />
        <div className="absolute -bottom-16 -right-12 h-48 w-48 -rotate-6 bg-secondary/20 blur-2xl animate-float" />
      </div>

      <div className="relative mx-auto max-w-6xl px-4 md:px-6 lg:px-8 py-16 md:py-20 lg:py-24">
        <div className="grid md:grid-cols-2 gap-10 md:gap-12 items-center">
          <div className="space-y-6">
            <h1 className="text-pretty text-4xl md:text-5xl lg:text-6xl font-semibold text-foreground tracking-tight animate-reveal">
              Track money clearly. Grow wealth confidently.
            </h1>
            <p className="text-lg md:text-xl text-muted-foreground leading-relaxed max-w-xl animate-reveal [animation-delay:120ms]">
              A launch‑ready finance platform with clean insights, real‑time charts, and seamless workflows— designed
              with a modern SaaS aesthetic and built for clarity.
            </p>
            <div className="flex items-center gap-3 animate-reveal [animation-delay:220ms]">
              <Button className="bg-primary text-primary-foreground hover:opacity-90 transition">Get Started</Button>
              <Button variant="outline" className="border-border text-foreground hover:bg-secondary/10 bg-transparent">
                Live Demo
              </Button>
            </div>
            <div className="flex items-center gap-6 pt-6 opacity-90">
              <Image src="/trusted-logo-1.png" alt="Trusted brand 1" width={90} height={28} />
              <Image src="/trusted-logo-2.png" alt="Trusted brand 2" width={90} height={28} />
              <Image src="/trusted-logo-3.png" alt="Trusted brand 3" width={90} height={28} />
            </div>
          </div>

          <div className="relative">
            <div className="absolute -inset-4 rounded-2xl border border-border/60 bg-background/40 backdrop-blur-sm" />
            <div className="relative rounded-xl overflow-hidden">
              <DashboardPreview />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
