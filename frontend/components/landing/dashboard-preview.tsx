"use client"

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, XAxis, YAxis } from "recharts"
import { Card, CardContent } from "@/components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { month: "Jan", inflow: 4200, outflow: 3100 },
  { month: "Feb", inflow: 4800, outflow: 3400 },
  { month: "Mar", inflow: 5300, outflow: 3600 },
  { month: "Apr", inflow: 5100, outflow: 3900 },
  { month: "May", inflow: 6200, outflow: 4200 },
  { month: "Jun", inflow: 6800, outflow: 4600 },
]

export default function DashboardPreview() {
  return (
    <Card className="border border-border/60 shadow-sm bg-card animate-reveal">
      <CardContent className="p-4 md:p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="space-y-1">
            <p className="text-sm text-muted-foreground">Monthly Balance</p>
            <h3 className="text-xl font-semibold text-foreground">$8,420</h3>
          </div>
          <span className="rounded-full px-2 py-1 text-xs font-medium bg-primary/10 text-primary">12% MoM</span>
        </div>
        <ChartContainer
          config={{
            inflow: { label: "Inflow", color: "hsl(var(--chart-1))" },
            outflow: { label: "Outflow", color: "hsl(var(--chart-2))" },
          }}
          className="h-[200px] md:h-[260px]"
        >
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="inflow" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--color-inflow)" stopOpacity={0.7} />
                  <stop offset="95%" stopColor="var(--color-inflow)" stopOpacity={0.05} />
                </linearGradient>
                <linearGradient id="outflow" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--color-outflow)" stopOpacity={0.5} />
                  <stop offset="95%" stopColor="var(--color-outflow)" stopOpacity={0.03} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="var(--border)" vertical={false} />
              <XAxis dataKey="month" tickLine={false} axisLine={false} />
              <YAxis tickLine={false} axisLine={false} hide />
              <ChartTooltip content={<ChartTooltipContent />} />
              <Area type="monotone" dataKey="inflow" stroke="var(--color-inflow)" fillOpacity={1} fill="url(#inflow)" />
              <Area
                type="monotone"
                dataKey="outflow"
                stroke="var(--color-outflow)"
                fillOpacity={1}
                fill="url(#outflow)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
