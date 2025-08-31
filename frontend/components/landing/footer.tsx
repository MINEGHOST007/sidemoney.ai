export default function SiteFooter() {
  return (
    <footer className="border-t border-border/60">
      <div className="mx-auto max-w-6xl px-4 md:px-6 lg:px-8 py-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <p className="text-sm text-muted-foreground">© {new Date().getFullYear()} sidemoney — All rights reserved.</p>
        <nav className="flex items-center gap-6 text-sm">
          <a className="text-muted-foreground hover:text-foreground" href="#features">
            Features
          </a>
          <a className="text-muted-foreground hover:text-foreground" href="#pricing">
            Pricing
          </a>
          <a className="text-muted-foreground hover:text-foreground" href="#security">
            Security
          </a>
        </nav>
      </div>
    </footer>
  )
}
