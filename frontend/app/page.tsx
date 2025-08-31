import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Navbar } from "@/components/navbar"
import { Check, Brain, ReceiptText, Target, ShieldCheck, Baseline as ChartLine, ArrowRight, Star } from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[rgb(8,7,14)] text-white font-inter">
      <Navbar />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4 pt-20">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 rounded-full bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.1)] px-4 py-2 text-sm font-medium text-white/80 mb-8">
            <span className="h-2 w-2 rounded-full bg-[rgb(0,255,178)]" />
            Beta — Free during launch
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent mb-6 leading-tight">
            Spend smarter.
            <br />
            Save faster.
          </h1>
          
          <p className="text-xl md:text-2xl text-white/70 mb-12 max-w-3xl mx-auto leading-relaxed">
            Real-time insights, AI-powered reports, and adaptive budgets—everything you need to manage money with confidence and hit your goals sooner.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link href="/login">
              <Button className="bg-[rgb(0,255,178)] text-black hover:bg-[rgb(0,255,178)]/90 px-8 py-4 text-lg font-semibold rounded-full transition-all duration-300 flex items-center gap-2">
                Start free
                <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
            <a href="#features">
              <Button variant="outline" className="border-white/20 text-white hover:bg-white/10 px-8 py-4 text-lg rounded-full bg-transparent">
                See features
              </Button>
            </a>
          </div>

          {/* Feature highlights */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-sm text-white/60">
            {[
              "AI daily spending reports",
              "OCR receipt import", 
              "Goals tracking with progress",
              "Secure Google sign-in",
            ].map((feature) => (
              <div key={feature} className="flex items-center gap-2">
                <Check className="h-4 w-4 text-[rgb(0,255,178)]" />
                <span>{feature}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-[rgb(0,255,178)]/5 via-transparent to-[rgb(255,0,102)]/5 pointer-events-none" />
      </section>

      {/* Introduction Section */}
      <section id="intro" className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Why choose sidemoney?
            </h2>
            <p className="text-xl text-white/70 max-w-3xl mx-auto">
              Built for modern savers who want intelligent insights without the complexity.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="space-y-8">
                {[
                  {
                    icon: Brain,
                    title: "AI-Powered Intelligence",
                    description: "Get personalized spending insights and recommendations that actually help you save money."
                  },
                  {
                    icon: Target, 
                    title: "Goal-Oriented Planning",
                    description: "Set clear financial goals and track your progress with intelligent budgeting."
                  },
                  {
                    icon: ShieldCheck,
                    title: "Bank-Level Security", 
                    description: "Your financial data is protected with enterprise-grade security and encryption."
                  }
                ].map(({ icon: Icon, title, description }) => (
                  <div key={title} className="flex gap-4">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 rounded-full bg-[rgb(0,255,178)]/10 flex items-center justify-center">
                        <Icon className="h-6 w-6 text-[rgb(0,255,178)]" />
                      </div>
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
                      <p className="text-white/70">{description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative">
              <div className="bg-[rgba(255,255,255,0.04)] rounded-2xl p-8 border border-white/10">
                <img 
                  src="/finance-dashboard-preview.png" 
                  alt="Finance dashboard preview" 
                  className="w-full rounded-lg"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-4 bg-[rgb(23,23,29)]">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Powerful features, thoughtfully designed
            </h2>
            <p className="text-xl text-white/70">
              Everything you need to take control of your finances.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { 
                icon: ChartLine, 
                title: "Smart Budgeting", 
                description: "Daily budgets that adapt to your income and goals automatically." 
              },
              { 
                icon: Brain, 
                title: "AI Insights", 
                description: "Get actionable suggestions to cut costs and grow your savings." 
              },
              { 
                icon: ReceiptText, 
                title: "Receipt OCR", 
                description: "Snap a photo to log transactions in seconds with AI recognition." 
              },
              { 
                icon: Target, 
                title: "Clear Goals", 
                description: "Plan ahead with progress tracking, dates, and contribution planning." 
              },
              { 
                icon: ShieldCheck, 
                title: "Secure & Private", 
                description: "Google sign-in with JWT authentication. Your data stays protected." 
              },
              { 
                icon: Check, 
                title: "Simple to Use", 
                description: "Clean design, zero clutter, and fast to set up and start using." 
              },
            ].map(({ icon: Icon, title, description }) => (
              <div key={title} className="group">
                <div className="bg-[rgba(255,255,255,0.04)] rounded-xl p-6 border border-white/10 hover:border-[rgb(0,255,178)]/30 transition-all duration-300 hover:transform hover:-translate-y-1">
                  <div className="w-12 h-12 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center mb-4 group-hover:bg-[rgb(0,255,178)]/20 transition-colors">
                    <Icon className="h-6 w-6 text-[rgb(0,255,178)]" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3">{title}</h3>
                  <p className="text-white/70 leading-relaxed">{description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="howitworks" className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              How it works
            </h2>
            <p className="text-xl text-white/70">
              Get started in minutes, see results immediately.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: "01",
                title: "Connect & Setup",
                description: "Sign up with Google and set your initial budget and financial goals."
              },
              {
                step: "02", 
                title: "Track Expenses",
                description: "Add transactions manually or snap photos of receipts for instant OCR processing."
              },
              {
                step: "03",
                title: "Get Insights",
                description: "Receive AI-powered daily reports and recommendations to optimize your spending."
              }
            ].map(({ step, title, description }) => (
              <div key={step} className="text-center">
                <div className="w-16 h-16 rounded-full bg-gradient-to-r from-[rgb(0,255,178)] to-[rgb(0,255,178)]/70 flex items-center justify-center text-black font-bold text-xl mx-auto mb-6">
                  {step}
                </div>
                <h3 className="text-2xl font-semibold text-white mb-4">{title}</h3>
                <p className="text-white/70 leading-relaxed">{description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-24 px-4 bg-[rgb(23,23,29)]">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              What our users say
            </h2>
            <p className="text-xl text-white/70">
              Join thousands of users already saving smarter.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                name: "Sarah Chen",
                role: "Freelance Designer",
                content: "Finally, a finance app that actually helps me save money instead of just tracking it. The AI insights are spot-on.",
                rating: 5
              },
              {
                name: "Mike Rodriguez", 
                role: "Software Engineer",
                content: "The OCR feature is a game-changer. I just snap photos of receipts and everything is categorized automatically.",
                rating: 5
              },
              {
                name: "Emily Johnson",
                role: "Marketing Manager", 
                content: "I've tried so many budgeting apps, but this is the first one that actually adapts to my changing income and goals.",
                rating: 5
              }
            ].map(({ name, role, content, rating }) => (
              <div key={name} className="bg-[rgba(255,255,255,0.04)] rounded-xl p-6 border border-white/10">
                <div className="flex gap-1 mb-4">
                  {[...Array(rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 fill-[rgb(0,255,178)] text-[rgb(0,255,178)]" />
                  ))}
                </div>
                <p className="text-white/80 mb-6 leading-relaxed">"{content}"</p>
                <div>
                  <div className="font-semibold text-white">{name}</div>
                  <div className="text-white/60">{role}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-24 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Frequently asked questions
            </h2>
            <p className="text-xl text-white/70">
              Everything you need to know about sidemoney.
            </p>
          </div>

          <div className="space-y-6">
            {[
              {
                question: "Is sidemoney really free during beta?",
                answer: "Yes! sidemoney is completely free while we're in beta. We want to gather feedback and perfect the experience before launching our paid plans."
              },
              {
                question: "How secure is my financial data?",
                answer: "We use bank-level encryption and security measures. Your data is encrypted both in transit and at rest, and we never store your actual bank credentials."
              },
              {
                question: "Can I import data from other budgeting apps?",
                answer: "Currently, we support manual entry and receipt OCR. We're working on import features for popular apps like Mint and YNAB."
              },
              {
                question: "How accurate is the AI spending analysis?",
                answer: "Our AI learns from your spending patterns and becomes more accurate over time. Most users see relevant insights within their first week of use."
              }
            ].map(({ question, answer }) => (
              <div key={question} className="bg-[rgba(255,255,255,0.04)] rounded-xl p-6 border border-white/10">
                <h3 className="text-xl font-semibold text-white mb-3">{question}</h3>
                <p className="text-white/70 leading-relaxed">{answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-24 px-4 bg-gradient-to-r from-[rgb(0,255,178)]/10 to-[rgb(255,0,102)]/10">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to take control of your finances?
          </h2>
          <p className="text-xl text-white/70 mb-12 max-w-2xl mx-auto">
            Join thousands of users already saving smarter with AI-powered insights and intelligent budgeting.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/login">
              <Button className="bg-[rgb(0,255,178)] text-black hover:bg-[rgb(0,255,178)]/90 px-8 py-4 text-lg font-semibold rounded-full transition-all duration-300 flex items-center gap-2">
                Start free today
                <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
            <p className="text-white/60 text-sm">No credit card required • Free during beta</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 bg-[rgb(8,7,14)]">
        <div className="max-w-6xl mx-auto px-4 py-12">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="text-lg font-semibold text-white mb-4">sidemoney</h3>
              <p className="text-white/60 text-sm">
                Smart financial management for the modern saver.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Product</h4>
              <div className="space-y-2 text-sm text-white/60">
                <a href="#features" className="block hover:text-white transition-colors">Features</a>
                <a href="#howitworks" className="block hover:text-white transition-colors">How it works</a>
                <a href="#pricing" className="block hover:text-white transition-colors">Pricing</a>
              </div>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Company</h4>
              <div className="space-y-2 text-sm text-white/60">
                <a href="#" className="block hover:text-white transition-colors">About</a>
                <a href="#" className="block hover:text-white transition-colors">Blog</a>
                <a href="#" className="block hover:text-white transition-colors">Careers</a>
              </div>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Support</h4>
              <div className="space-y-2 text-sm text-white/60">
                <a href="#faq" className="block hover:text-white transition-colors">FAQ</a>
                <a href="#" className="block hover:text-white transition-colors">Contact</a>
                <a href="#" className="block hover:text-white transition-colors">Privacy</a>
              </div>
            </div>
          </div>
          
          <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <span className="text-white/60 text-sm">© {new Date().getFullYear()} sidemoney. All rights reserved.</span>
            <div className="flex gap-6 text-white/60 text-sm">
              <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
              <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
