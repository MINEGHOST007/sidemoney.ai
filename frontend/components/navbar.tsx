"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useAuth } from "@/context/auth-context"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { 
  LayoutDashboard, 
  Receipt, 
  Target, 
  TrendingUp, 
  Settings,
  LogOut,
  Menu,
  X
} from "lucide-react"
import { useState } from "react"

export function Navbar() {
  const { user, logout } = useAuth()
  const pathname = usePathname()
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  
  const isDashboard = pathname?.startsWith('/dashboard') || pathname?.startsWith('/app')
  
  // Dashboard navigation items
  const dashboardNavItems = [
    { href: "/dashboard", label: "Overview", icon: LayoutDashboard },
    { href: "/dashboard/transactions", label: "Transactions", icon: Receipt },
    { href: "/dashboard/goals", label: "Goals", icon: Target },
    { href: "/dashboard/analytics", label: "Analytics", icon: TrendingUp },
  ]
  
  // Landing page navigation items
  const landingNavItems = [
    { href: "#features", label: "Features" },
    { href: "#howitworks", label: "How it works" },
    { href: "#testimonials", label: "Testimonials" },
    { href: "#faq", label: "FAQ" },
  ]

  return (
    <header className={`fixed top-0 w-full z-50 backdrop-blur-sm border-b transition-colors ${
      isDashboard 
        ? 'bg-[rgb(8,7,14)]/98 border-white/10' 
        : 'bg-[rgb(8,7,14)]/95 border-white/10'
    }`}>
      <div className="mx-auto max-w-7xl px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href={user ? "/dashboard" : "/"} className="flex items-center gap-3">
            
            <span className="font-bold text-2xl text-white tracking-tight">sidemoney</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {isDashboard ? (
              // Dashboard Navigation
              dashboardNavItems.map(({ href, label, icon: Icon }) => {
                const isActive = pathname === href
                return (
                  <Link key={href} href={href}>
                    <Button 
                      variant="ghost" 
                      className={`flex items-center gap-2 px-4 py-2 text-sm transition-all duration-200 ${
                        isActive 
                          ? 'bg-[rgb(0,255,178)]/10 text-[rgb(0,255,178)] hover:bg-[rgb(0,255,178)]/15' 
                          : 'text-white/70 hover:text-white hover:bg-white/5'
                      }`}
                    >
                      <Icon className="h-4 w-4" />
                      {label}
                    </Button>
                  </Link>
                )
              })
            ) : (
              // Landing Page Navigation
              landingNavItems.map(({ href, label }) => (
                <Link key={href} href={href}>
                  <Button 
                    variant="ghost" 
                    className="text-white/70 hover:text-white hover:bg-white/5 px-4 py-2 text-sm transition-colors"
                  >
                    {label}
                  </Button>
                </Link>
              ))
            )}
          </nav>

          {/* Right Side */}
          <div className="flex items-center gap-3">
            {!user ? (
              // Unauthenticated state
              <>
                <Link href="/login" className="hidden sm:inline-block">
                  <Button variant="ghost" className="text-white/70 hover:text-white hover:bg-white/10 px-4 py-2">
                    Sign in
                  </Button>
                </Link>
                <Link href="/login">
                  <Button className="bg-[rgb(0,255,178)] text-black hover:bg-[rgb(0,255,178)]/90 font-semibold rounded-full px-6 py-2 transition-all duration-200 shadow-lg shadow-[rgb(0,255,178)]/20">
                    Get started
                  </Button>
                </Link>
              </>
            ) : (
              // Authenticated state
              <>
                {!isDashboard && (
                  <Link href="/dashboard">
                    <Button className="bg-[rgb(0,255,178)]/10 text-[rgb(0,255,178)] hover:bg-[rgb(0,255,178)]/20 border border-[rgb(0,255,178)]/20 px-4 py-2 rounded-full transition-colors">
                      Dashboard
                    </Button>
                  </Link>
                )}
                
                {/* User Menu */}
                <div className="flex items-center gap-2">
                  <Avatar className="h-9 w-9 border-2 border-white/10">
                    <AvatarImage src={user.avatar_url || ""} alt={user.name || "User"} />
                    <AvatarFallback className="bg-gradient-to-r from-[rgb(0,255,178)]/20 to-[rgb(255,0,102)]/20 text-white font-semibold">
                      {user.name?.[0]?.toUpperCase() || "U"}
                    </AvatarFallback>
                  </Avatar>
                  
                  {isDashboard && (
                    <>
                      <Button variant="ghost" size="sm" className="hidden md:flex text-white/70 hover:text-white hover:bg-white/5">
                        <Settings className="h-4 w-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={logout}
                        className="hidden md:flex text-white/70 hover:text-white hover:bg-white/5"
                      >
                        <LogOut className="h-4 w-4" />
                      </Button>
                    </>
                  )}
                </div>
              </>
            )}

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden text-white hover:bg-white/10"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="lg:hidden mt-4 pb-4 border-t border-white/10">
            <nav className="flex flex-col gap-2 mt-4">
              {isDashboard ? (
                // Dashboard Mobile Navigation
                <>
                  {dashboardNavItems.map(({ href, label, icon: Icon }) => {
                    const isActive = pathname === href
                    return (
                      <Link key={href} href={href} onClick={() => setIsMenuOpen(false)}>
                        <Button 
                          variant="ghost" 
                          className={`w-full justify-start gap-3 py-3 ${
                            isActive 
                              ? 'bg-[rgb(0,255,178)]/10 text-[rgb(0,255,178)]' 
                              : 'text-white/70 hover:text-white hover:bg-white/5'
                          }`}
                        >
                          <Icon className="h-4 w-4" />
                          {label}
                        </Button>
                      </Link>
                    )
                  })}
                  <hr className="border-white/10 my-2" />
                  <Button 
                    variant="ghost" 
                    className="w-full justify-start gap-3 py-3 text-white/70 hover:text-white hover:bg-white/5"
                  >
                    <Settings className="h-4 w-4" />
                    Settings
                  </Button>
                  <Button 
                    variant="ghost" 
                    onClick={logout}
                    className="w-full justify-start gap-3 py-3 text-white/70 hover:text-white hover:bg-white/10"
                  >
                    <LogOut className="h-4 w-4" />
                    Logout
                  </Button>
                </>
              ) : (
                // Landing Page Mobile Navigation
                <>
                  {landingNavItems.map(({ href, label }) => (
                    <Link key={href} href={href} onClick={() => setIsMenuOpen(false)}>
                      <Button variant="ghost" className="w-full justify-start py-3 text-white/70 hover:text-white hover:bg-white/5">
                        {label}
                      </Button>
                    </Link>
                  ))}
                  {!user && (
                    <>
                      <hr className="border-white/10 my-2" />
                      <Link href="/login" onClick={() => setIsMenuOpen(false)}>
                        <Button variant="ghost" className="w-full justify-start py-3 text-white/70 hover:text-white hover:bg-white/5">
                          Sign in
                        </Button>
                      </Link>
                      <Link href="/login" onClick={() => setIsMenuOpen(false)}>
                        <Button className="w-full mt-2 bg-[rgb(0,255,178)] text-black hover:bg-[rgb(0,255,178)]/90 font-semibold rounded-full py-3">
                          Get started
                        </Button>
                      </Link>
                    </>
                  )}
                </>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}
