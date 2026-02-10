export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute w-96 h-96 bg-electric-mint opacity-10 rounded-full blur-3xl top-1/4 left-1/4 animate-pulse"></div>
          <div className="absolute w-96 h-96 bg-electric-mint opacity-10 rounded-full blur-3xl bottom-1/4 right-1/4 animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>

        <div className="relative z-10 max-w-6xl mx-auto px-6 text-center">
          {/* Logo */}
          <div className="mb-8 flex justify-center">
            <div className="glass-card px-8 py-4 rounded-full inline-block">
              <h1 className="text-4xl font-bold">
                <span className="text-electric-mint">Split</span>
                <span>Mint</span>
              </h1>
            </div>
          </div>

          {/* Tagline */}
          <h2 className="text-6xl md:text-7xl font-bold mb-6 leading-tight">
            Split Expenses
            <br />
            <span className="text-electric-mint">Mint Fresh</span>
          </h2>

          <p className="text-xl text-slate-grey mb-12 max-w-2xl mx-auto">
            The smartest way to share expenses with friends. AI-powered parsing,
            smart debt settlement, and real-time balance updates.
          </p>

          {/* CTA Buttons */}
          <div className="flex gap-4 justify-center flex-wrap">
            <a href="/dashboard" className="btn-primary inline-flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Get Started Free
            </a>
            <a href="#features" className="btn-secondary inline-flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
              Learn More
            </a>
          </div>

          {/* Stats */}
          <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
            <div className="glass-card p-6 rounded-2xl">
              <div className="text-4xl font-bold text-electric-mint mb-2">$0</div>
              <div className="text-slate-grey">Transaction Fees</div>
            </div>
            <div className="glass-card p-6 rounded-2xl">
              <div className="text-4xl font-bold text-electric-mint mb-2">AI</div>
              <div className="text-slate-grey">Powered Parsing</div>
            </div>
            <div className="glass-card p-6 rounded-2xl">
              <div className="text-4xl font-bold text-electric-mint mb-2">Real-time</div>
              <div className="text-slate-grey">Balance Updates</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h3 className="text-4xl font-bold mb-4">Powerful Features</h3>
            <p className="text-slate-grey text-lg">Everything you need to manage shared expenses</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="glass-card p-8 rounded-2xl hover:border-electric-mint transition-all group">
              <div className="w-12 h-12 bg-electric-mint bg-opacity-20 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-electric-mint" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h4 className="text-xl font-semibold mb-3">MintSense AI</h4>
              <p className="text-slate-grey">
                Just type &quot;Paid $120 for dinner with Alice&quot; and let AI parse the details for you.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="glass-card p-8 rounded-2xl hover:border-electric-mint transition-all group">
              <div className="w-12 h-12 bg-electric-mint bg-opacity-20 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-electric-mint" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <h4 className="text-xl font-semibold mb-3">Smart Splits</h4>
              <p className="text-slate-grey">
                Equal, custom amounts, or percentages. Perfect penny-level accuracy every time.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="glass-card p-8 rounded-2xl hover:border-electric-mint transition-all group">
              <div className="w-12 h-12 bg-electric-mint bg-opacity-20 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-electric-mint" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <h4 className="text-xl font-semibold mb-3">Debt Simplification</h4>
              <p className="text-slate-grey">
                Minimize transactions with our smart algorithm. Less hassle, faster settlements.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="glass-card p-8 rounded-2xl hover:border-electric-mint transition-all group">
              <div className="w-12 h-12 bg-electric-mint bg-opacity-20 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-electric-mint" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h4 className="text-xl font-semibold mb-3">Real-time Updates</h4>
              <p className="text-slate-grey">
                See balances update instantly across all devices. No more outdated information.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="glass-card p-8 rounded-2xl hover:border-electric-mint transition-all group">
              <div className="w-12 h-12 bg-electric-mint bg-opacity-20 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-electric-mint" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h4 className="text-xl font-semibold mb-3">Secure & Private</h4>
              <p className="text-slate-grey">
                Bank-level security with Clerk authentication. Your data stays private.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="glass-card p-8 rounded-2xl hover:border-electric-mint transition-all group">
              <div className="w-12 h-12 bg-electric-mint bg-opacity-20 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-electric-mint" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <h4 className="text-xl font-semibold mb-3">Ledger-based</h4>
              <p className="text-slate-grey">
                Immutable transaction history. Full audit trail for complete transparency.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-6">
        <div className="max-w-4xl mx-auto text-center glass-card p-12 rounded-3xl">
          <h3 className="text-4xl font-bold mb-4">Ready to simplify your expenses?</h3>
          <p className="text-slate-grey text-lg mb-8">
            Join thousands of users who trust SplitMint for their shared expenses.
          </p>
          <a href="/dashboard" className="btn-primary inline-flex items-center gap-2 text-lg">
            Start Using SplitMint
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12 px-6">
        <div className="max-w-6xl mx-auto text-center text-slate-grey">
          <p className="mb-4">
            <span className="text-electric-mint font-semibold">SplitMint</span> - Gateway to Karbon
          </p>
          <p className="text-sm">Built with Next.js, FastAPI, and PostgreSQL</p>
        </div>
      </footer>
    </div>
  );
}
