import Link from 'next/link'
import { ArrowRight, Plane, BookOpen, BarChart3, FileText, Brain, Shield, Star, Zap, Users, TrendingUp, Award } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0A0F1E] text-white">
      {/* Navigation */}
      <nav className="border-b border-white/10 backdrop-blur-sm fixed top-0 w-full z-50 bg-[#0A0F1E]/80">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-[#0099CC] to-[#003087] rounded-xl flex items-center justify-center">
              <Plane className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="font-bold text-xl text-white">AROS</span>
              <p className="text-xs text-[#0099CC] -mt-0.5">Aviation Research OS</p>
            </div>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm text-gray-400">
            <Link href="#features" className="hover:text-white transition-colors">Features</Link>
            <Link href="#agents" className="hover:text-white transition-colors">AI Agents</Link>
            <Link href="#modules" className="hover:text-white transition-colors">Modules</Link>
            <Link href="#pricing" className="hover:text-white transition-colors">Pricing</Link>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/dashboard" className="text-sm text-gray-400 hover:text-white transition-colors px-4 py-2">
              Sign In
            </Link>
            <Link href="/dashboard" className="bg-[#0099CC] hover:bg-[#007AA3] text-white text-sm font-medium px-5 py-2.5 rounded-lg transition-colors flex items-center gap-2">
              Get Started <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-24 px-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#003087]/20 via-transparent to-[#0099CC]/10 pointer-events-none" />
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-[#0099CC]/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-[#003087]/10 rounded-full blur-3xl" />

        <div className="max-w-5xl mx-auto text-center relative">
          <div className="inline-flex items-center gap-2 bg-[#0099CC]/10 border border-[#0099CC]/20 rounded-full px-4 py-2 text-sm text-[#0099CC] mb-8">
            <Zap className="w-4 h-4" />
            The First AI-Native Aviation Research Platform
          </div>

          <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-6">
            <span className="text-white">Aviation Research,</span>
            <br />
            <span className="bg-gradient-to-r from-[#0099CC] via-[#00B4D8] to-[#FFB300] bg-clip-text text-transparent">
              Reimagined with AI
            </span>
          </h1>

          <p className="text-xl text-gray-400 max-w-3xl mx-auto mb-4">
            AROS is the complete AI-powered research operating system for aviation management —
            from topic generation to Scopus publication. Built for Master&apos;s, PhD, and DBA researchers.
          </p>
          <p className="text-lg text-gray-500 max-w-2xl mx-auto mb-10">
            ระบบวิจัยด้านการบินที่ขับเคลื่อนด้วย AI สำหรับนักศึกษาปริญญาโท–เอก และนักวิจัยด้านการจัดการการบิน
          </p>

          <div className="flex items-center justify-center gap-4 flex-wrap">
            <Link href="/dashboard" className="bg-gradient-to-r from-[#0099CC] to-[#003087] hover:from-[#007AA3] hover:to-[#002266] text-white font-semibold px-8 py-4 rounded-xl text-lg transition-all flex items-center gap-2 shadow-lg shadow-[#0099CC]/20">
              Start Researching <ArrowRight className="w-5 h-5" />
            </Link>
            <Link href="#demo" className="border border-white/20 hover:border-white/40 text-white font-medium px-8 py-4 rounded-xl text-lg transition-all">
              Watch Demo
            </Link>
          </div>

          <div className="mt-12 flex items-center justify-center gap-8 text-sm text-gray-500">
            <div className="flex items-center gap-2">
              <Star className="w-4 h-4 text-[#FFB300]" />
              <span>12 Specialized AI Agents</span>
            </div>
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-[#0099CC]" />
              <span>Aviation Domain Expert</span>
            </div>
            <div className="flex items-center gap-2">
              <Award className="w-4 h-4 text-green-400" />
              <span>Scopus-Ready Output</span>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-6 border-y border-white/5">
        <div className="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8">
          {[
            { value: '12', label: 'AI Research Agents', icon: Brain },
            { value: '8+', label: 'Aviation Modules', icon: Plane },
            { value: '50+', label: 'Research Frameworks', icon: BarChart3 },
            { value: '1000+', label: 'Research Topics', icon: BookOpen },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <stat.icon className="w-8 h-8 text-[#0099CC] mx-auto mb-3" />
              <div className="text-4xl font-bold text-white mb-1">{stat.value}</div>
              <div className="text-gray-500 text-sm">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Research Workflow */}
      <section id="features" className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">Complete Research Lifecycle</h2>
            <p className="text-gray-400 text-lg">From idea to publication — all in one platform</p>
          </div>

          <div className="flex flex-wrap justify-center gap-3">
            {[
              { step: '01', label: 'Topic Generation', icon: '🎯' },
              { step: '02', label: 'Literature Review', icon: '📚' },
              { step: '03', label: 'Gap Detection', icon: '🔍' },
              { step: '04', label: 'Framework Design', icon: '🏗️' },
              { step: '05', label: 'Questionnaire', icon: '📋' },
              { step: '06', label: 'Data Collection', icon: '📊' },
              { step: '07', label: 'Statistical Analysis', icon: '📈' },
              { step: '08', label: 'Paper Writing', icon: '✍️' },
              { step: '09', label: 'Publication', icon: '📰' },
            ].map((item, i) => (
              <div key={item.step} className="flex items-center gap-2">
                <div className="flex flex-col items-center">
                  <div className="w-14 h-14 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-2xl hover:bg-[#0099CC]/10 hover:border-[#0099CC]/30 transition-all cursor-pointer">
                    {item.icon}
                  </div>
                  <span className="text-xs text-gray-500 mt-1 text-center max-w-[70px]">{item.label}</span>
                </div>
                {i < 8 && <div className="text-gray-700 text-xl mb-4">→</div>}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Agents Section */}
      <section id="agents" className="py-24 px-6 bg-white/2">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">12 Specialized AI Agents</h2>
            <p className="text-gray-400 text-lg">Each agent is an expert in its domain</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {agents.map((agent) => (
              <div key={agent.id} className="p-5 rounded-xl bg-white/3 border border-white/8 hover:border-[#0099CC]/30 transition-all group">
                <div className="flex items-start gap-4">
                  <div className="text-3xl">{agent.icon}</div>
                  <div className="flex-1">
                    <h3 className="text-white font-semibold mb-1">{agent.name}</h3>
                    <p className="text-gray-500 text-sm mb-3">{agent.desc}</p>
                    <div className="flex flex-wrap gap-1">
                      {agent.tags.map((tag) => (
                        <span key={tag} className="text-xs px-2 py-0.5 rounded-full bg-[#0099CC]/10 text-[#0099CC] border border-[#0099CC]/20">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-10">
            <Link href="/dashboard" className="inline-flex items-center gap-2 bg-[#0099CC] hover:bg-[#007AA3] text-white font-medium px-8 py-3 rounded-xl transition-colors">
              Access All Agents <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Aviation Modules */}
      <section id="modules" className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">Aviation Domain Modules</h2>
            <p className="text-gray-400">Deep knowledge base for every aviation research area</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {modules.map((mod) => (
              <div key={mod.id} className="p-5 rounded-xl bg-white/3 border border-white/8 hover:border-[#FFB300]/30 transition-all text-center group cursor-pointer">
                <div className="text-4xl mb-3">{mod.icon}</div>
                <h3 className="text-white font-medium text-sm mb-1">{mod.name}</h3>
                <p className="text-gray-500 text-xs">{mod.topics}+ research topics</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* For Researchers */}
      <section className="py-24 px-6 bg-gradient-to-b from-transparent to-[#003087]/10">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">Built for Aviation Researchers</h2>
            <p className="text-gray-400">Designed specifically for CATC, university programs, and aviation industry research</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                icon: Users,
                title: "Master's Students (ป.โท)",
                desc: "Generate research topics, build frameworks, create questionnaires, and write complete thesis chapters",
                color: "text-[#0099CC]",
              },
              {
                icon: TrendingUp,
                title: "PhD & DBA Candidates",
                desc: "Advanced SEM/CFA analysis, systematic literature review, Scopus paper preparation",
                color: "text-[#FFB300]",
              },
              {
                icon: BookOpen,
                title: "Aviation Lecturers",
                desc: "Create course materials, research guidance tools, and publish in Q1/Q2 aviation journals",
                color: "text-green-400",
              },
            ].map((item) => (
              <div key={item.title} className="p-6 rounded-xl bg-white/3 border border-white/8">
                <item.icon className={`w-10 h-10 ${item.color} mb-4`} />
                <h3 className="text-white font-semibold text-lg mb-2">{item.title}</h3>
                <p className="text-gray-400 text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Start Your Aviation Research Journey
          </h2>
          <p className="text-gray-400 text-lg mb-8">
            เริ่มต้นการวิจัยด้านการบินของคุณด้วย AI ที่ทรงพลังที่สุด
          </p>
          <Link href="/dashboard" className="inline-flex items-center gap-2 bg-gradient-to-r from-[#0099CC] to-[#003087] text-white font-semibold px-10 py-4 rounded-xl text-lg transition-all hover:shadow-lg hover:shadow-[#0099CC]/20">
            Launch AROS Platform <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Plane className="w-6 h-6 text-[#0099CC]" />
            <span className="text-white font-semibold">AROS</span>
            <span className="text-gray-600 text-sm">Aviation Research Operating System</span>
          </div>
          <p className="text-gray-600 text-sm">
            © 2026 AROS. Advancing Aviation Research with AI.
          </p>
        </div>
      </footer>
    </div>
  )
}

const agents = [
  { id: '1', icon: '🎯', name: 'Topic Generator', desc: 'Generate novel aviation research topics', tags: ['Novelty', 'Gap Detection'] },
  { id: '2', icon: '📚', name: 'Literature Review', desc: 'Search Scopus, WoS, Semantic Scholar', tags: ['Scopus', 'WoS'] },
  { id: '3', icon: '🕸️', name: 'Citation Mapping', desc: 'Build citation graphs and bibliometrics', tags: ['Citation Graph', 'Bibliometrics'] },
  { id: '4', icon: '🔍', name: 'Research Gap', desc: 'Detect underexplored research areas', tags: ['Gap Analysis', 'Trends'] },
  { id: '5', icon: '🏗️', name: 'Framework Builder', desc: 'Design TAM, UTAUT, SERVQUAL frameworks', tags: ['TAM', 'SEM'] },
  { id: '6', icon: '📋', name: 'Questionnaire Builder', desc: 'Generate Thai-English Likert questionnaires', tags: ['Bilingual', 'Validated'] },
  { id: '7', icon: '📊', name: 'Data Analysis', desc: 'SEM, CFA, PLS-SEM, APA tables', tags: ['SEM', 'CFA', 'PLS'] },
  { id: '8', icon: '✍️', name: 'Paper Writer', desc: 'Write complete thesis chapters 1-5', tags: ['APA 7th', 'Chapter 1-5'] },
  { id: '9', icon: '📰', name: 'Publication Agent', desc: 'Journal matching and cover letters', tags: ['Journal Match', 'Q1/Q2'] },
  { id: '10', icon: '👨‍🏫', name: 'Thesis Supervisor', desc: 'AI advisor feedback on your thesis', tags: ['Review', 'Feedback'] },
  { id: '11', icon: '🔬', name: 'SEM Expert', desc: 'CR, AVE, HTMT validation specialist', tags: ['CR/AVE', 'HTMT'] },
  { id: '12', icon: '✈️', name: 'Aviation Knowledge', desc: 'ICAO, IATA, and aviation standards', tags: ['ICAO', 'IATA'] },
]

const modules = [
  { id: '1', icon: '✈️', name: 'Airline Management', topics: 245 },
  { id: '2', icon: '🏢', name: 'Airport Management', topics: 189 },
  { id: '3', icon: '📦', name: 'Air Cargo & Logistics', topics: 156 },
  { id: '4', icon: '🛡️', name: 'Aviation Safety', topics: 201 },
  { id: '5', icon: '💻', name: 'Aviation Technology', topics: 178 },
  { id: '6', icon: '🌱', name: 'Sustainability', topics: 134 },
  { id: '7', icon: '👥', name: 'Passenger Experience', topics: 167 },
  { id: '8', icon: '📈', name: 'Air Transport Economics', topics: 143 },
]
