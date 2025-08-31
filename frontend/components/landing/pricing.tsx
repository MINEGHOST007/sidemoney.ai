import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function Pricing() {
  return (
    <section className="mx-auto max-w-6xl px-4 md:px-6 lg:px-8 py-12 md:py-16">
      <div className="mb-8 text-center">
        <h2 className="text-3xl md:text-4xl font-semibold text-foreground text-pretty">Simple, fair pricing</h2>
        <p className="text-muted-foreground mt-2">Start free. Upgrade when you’re ready.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Card className="border border-border/60 bg-card">
          <CardHeader>
            <CardTitle>Starter</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-4xl font-semibold text-foreground">$0</p>
            <ul className="text-sm text-muted-foreground list-disc pl-5 space-y-2">
              <li>Up to 1,000 transactions</li>
              <li>Basic analytics</li>
              <li>Email support</li>
            </ul>
            <Button className="w-full bg-primary text-primary-foreground hover:opacity-90">Get Started</Button>
          </CardContent>
        </Card>

        <Card className="border border-border/60 bg-card relative">
          <div className="absolute -top-3 right-4 rounded-full bg-secondary text-secondary-foreground text-xs px-2 py-1">
            Popular
          </div>
          <CardHeader>
            <CardTitle>Pro</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-4xl font-semibold text-foreground">
              $12<span className="text-base">/mo</span>
            </p>
            <ul className="text-sm text-muted-foreground list-disc pl-5 space-y-2">
              <li>Unlimited transactions</li>
              <li>Advanced analytics</li>
              <li>Priority support</li>
            </ul>
            <Button className="w-full bg-secondary text-secondary-foreground hover:opacity-90">Start Free Trial</Button>
          </CardContent>
        </Card>
      </div>
    </section>
  )
}
