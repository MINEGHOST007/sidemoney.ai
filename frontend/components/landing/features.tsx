import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ShieldCheck, LineChart, Sparkles } from "lucide-react"

export default function Features() {
  const items = [
    {
      icon: <LineChart className="h-5 w-5 text-primary" />,
      title: "Live Insights",
      desc: "Understand income, spend, and trends at a glance with elegant visuals.",
    },
    {
      icon: <ShieldCheck className="h-5 w-5 text-secondary" />,
      title: "Private by Design",
      desc: "Secure architecture with clear controls and transparent data handling.",
    },
    {
      icon: <Sparkles className="h-5 w-5 text-primary" />,
      title: "Delightful UX",
      desc: "Fast, fluid, and accessible. Built with a refined SaaS design system.",
    },
  ]

  return (
    <section className="mx-auto max-w-6xl px-4 md:px-6 lg:px-8 py-12 md:py-16">
      <div className="flex items-center gap-3 mb-6">
        <Badge className="bg-secondary text-secondary-foreground">Why choose us</Badge>
        <span className="text-sm text-muted-foreground">Modern, focused, and launch-ready</span>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {items.map((it) => (
          <Card key={it.title} className="border border-border/60 bg-card hover:-translate-y-0.5 transition">
            <CardHeader>
              <div className="flex items-center gap-2">
                {it.icon}
                <CardTitle>{it.title}</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">{it.desc}</CardContent>
          </Card>
        ))}
      </div>
    </section>
  )
}
