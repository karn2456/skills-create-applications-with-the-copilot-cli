import {
  BookOpen, Brain, FileText, TrendingUp, Plane,
  BarChart3, Clock, ArrowRight, Star, Zap, Target
} from 'lucide-react'
import Link from 'next/link'

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">
            สวัสดี, นักวิจัย! 👋
          </h1>
          <p className="text-gray-500 mt-1">
            Aviation Research Operating System — Ready to advance your research
          </p>
        </div>
        <Link href="/agents/topic-generator" className="flex items-center gap-2 bg-[#0099CC] hover:bg-[#007AA3] text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors">
          <Zap className="w-4 h-4" />
          New Research
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="p-5 rounded-xl bg-white/3 border border-white/8 hover:border-white/15 transition-all">
            <div className="flex items-center justify-between mb-3">
              <stat.icon className={`w-5 h-5 ${stat.color}`} />
              <span className={`text-xs px-2 py-0.5 rounded-full ${stat.badgeColor} ${stat.badgeText}`}>
                {stat.change}
              </span>
            </div>
            <div className="text-3xl font-bold text-white mb-0.5">{stat.value}</div>
            <div className="text-gray-500 text-sm">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
          Quick Actions — เริ่มต้นด่วน
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {quickActions.map((action) => (
            <Link
              key={action.href}
              href={action.href}
              className="p-4 rounded-xl bg-white/3 border border-white/8 hover:border-[#0099CC]/30 hover:bg-[#0099CC]/5 transition-all text-center group"
            >
              <div className="text-2xl mb-2">{action.icon}</div>
              <p className="text-xs text-gray-400 group-hover:text-white transition-colors font-medium">{action.label}</p>
            </Link>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Projects */}
        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-white font-semibold">Active Research Projects</h2>
            <Link href="/projects" className="text-[#0099CC] text-sm hover:text-[#00B4D8] flex items-center gap-1">
              View all <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
          <div className="space-y-3">
            {projects.map((project) => (
              <div key={project.id} className="p-4 rounded-xl bg-white/3 border border-white/8 hover:border-white/15 transition-all">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs px-2 py-0.5 rounded-full bg-[#0099CC]/10 text-[#0099CC] border border-[#0099CC]/20">
                        {project.domain}
                      </span>
                      <span className={`text-xs px-2 py-0.5 rounded-full ${project.levelColor}`}>
                        {project.level}
                      </span>
                    </div>
                    <h3 className="text-white text-sm font-medium">{project.title}</h3>
                  </div>
                  <span className="text-xs text-gray-600 ml-3">{project.lastUpdated}</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex-1 bg-white/10 rounded-full h-1.5">
                    <div
                      className="h-1.5 rounded-full bg-gradient-to-r from-[#0099CC] to-[#003087]"
                      style={{ width: `${project.progress}%` }}
                    />
                  </div>
                  <span className="text-xs text-gray-500 w-8 text-right">{project.progress}%</span>
                  <span className="text-xs text-gray-600">{project.currentStage}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-4">
          {/* AI Agents */}
          <div>
            <h2 className="text-white font-semibold mb-3">Featured Agents</h2>
            <div className="space-y-2">
              {featuredAgents.map((agent) => (
                <Link
                  key={agent.href}
                  href={agent.href}
                  className="flex items-center gap-3 p-3 rounded-lg bg-white/3 border border-white/8 hover:border-[#0099CC]/30 transition-all group"
                >
                  <span className="text-xl">{agent.icon}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-white text-sm font-medium truncate">{agent.name}</p>
                    <p className="text-gray-600 text-xs truncate">{agent.nameTh}</p>
                  </div>
                  <ArrowRight className="w-3 h-3 text-gray-700 group-hover:text-[#0099CC] transition-colors flex-shrink-0" />
                </Link>
              ))}
            </div>
          </div>

          {/* Research Trends */}
          <div className="p-4 rounded-xl bg-gradient-to-br from-[#003087]/20 to-[#0099CC]/10 border border-[#0099CC]/15">
            <div className="flex items-center gap-2 mb-3">
              <TrendingUp className="w-4 h-4 text-[#0099CC]" />
              <h3 className="text-white text-sm font-semibold">Hot Research Topics 2026</h3>
            </div>
            <div className="space-y-2">
              {trends.map((trend) => (
                <div key={trend} className="flex items-center gap-2 text-xs text-gray-400">
                  <Star className="w-3 h-3 text-[#FFB300]" />
                  {trend}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

const stats = [
  { label: 'Research Projects', value: '3', change: '+1 this month', icon: Brain, color: 'text-[#0099CC]', badgeColor: 'bg-blue-500/10', badgeText: 'text-blue-400' },
  { label: 'Papers Generated', value: '12', change: 'All time', icon: FileText, color: 'text-purple-400', badgeColor: 'bg-purple-500/10', badgeText: 'text-purple-400' },
  { label: 'Lit Reviews Done', value: '8', change: '+3 this week', icon: BookOpen, color: 'text-green-400', badgeColor: 'bg-green-500/10', badgeText: 'text-green-400' },
  { label: 'Avg Progress', value: '67%', change: 'Active', icon: BarChart3, color: 'text-[#FFB300]', badgeColor: 'bg-yellow-500/10', badgeText: 'text-yellow-400' },
]

const quickActions = [
  { href: '/agents/topic-generator', icon: '🎯', label: 'Generate Topic' },
  { href: '/agents/literature-review', icon: '📚', label: 'Lit Review' },
  { href: '/agents/framework-builder', icon: '🏗️', label: 'Build Framework' },
  { href: '/agents/questionnaire', icon: '📋', label: 'Questionnaire' },
  { href: '/agents/data-analysis', icon: '📊', label: 'Analyze Data' },
  { href: '/agents/paper-writing', icon: '✍️', label: 'Write Paper' },
]

const projects = [
  {
    id: 1,
    title: 'AI Adoption and Service Quality in Thai Airlines: A TAM Perspective',
    domain: 'Airline Management',
    level: 'PhD',
    levelColor: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
    progress: 75,
    currentStage: 'Analysis',
    lastUpdated: '2h ago',
  },
  {
    id: 2,
    title: 'Digital Transformation and Passenger Satisfaction at Suvarnabhumi Airport',
    domain: 'Airport Management',
    level: "Master's",
    levelColor: 'bg-green-500/10 text-green-400 border border-green-500/20',
    progress: 45,
    currentStage: 'Framework',
    lastUpdated: '1d ago',
  },
  {
    id: 3,
    title: 'Green Logistics and Carbon Reduction in Air Cargo Operations',
    domain: 'Air Cargo',
    level: 'DBA',
    levelColor: 'bg-orange-500/10 text-orange-400 border border-orange-500/20',
    progress: 30,
    currentStage: 'Literature',
    lastUpdated: '3d ago',
  },
]

const featuredAgents = [
  { icon: '🎯', name: 'Topic Generator', nameTh: 'สร้างหัวข้อวิจัย', href: '/agents/topic-generator' },
  { icon: '👨‍🏫', name: 'Thesis Supervisor', nameTh: 'อาจารย์ที่ปรึกษา AI', href: '/agents/thesis-supervisor' },
  { icon: '🔬', name: 'SEM/CFA Expert', nameTh: 'ผู้เชี่ยวชาญ SEM/CFA', href: '/agents/sem-expert' },
  { icon: '✈️', name: 'Aviation Knowledge', nameTh: 'ความรู้ด้านการบิน', href: '/agents/aviation-knowledge' },
]

const trends = [
  'AI & Digital Transformation in Airlines',
  'Sustainable Aviation Fuel Adoption',
  'Post-COVID Passenger Behavior',
  'Smart Airport Technology (IoT)',
  'Air Cargo E-commerce Growth',
]
