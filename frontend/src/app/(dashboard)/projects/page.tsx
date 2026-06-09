import Link from 'next/link'
import { Plus, Search, Filter, Plane, TrendingUp } from 'lucide-react'

export default function ProjectsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Research Projects</h1>
          <p className="text-gray-500 text-sm mt-1">โครงการวิจัยด้านการบินทั้งหมดของคุณ</p>
        </div>
        <button className="flex items-center gap-2 bg-[#0099CC] hover:bg-[#007AA3] text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors">
          <Plus className="w-4 h-4" />
          New Project
        </button>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-3">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            placeholder="Search projects..."
            className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-2 text-sm text-gray-300 placeholder-gray-600 focus:outline-none focus:border-[#0099CC]/40"
          />
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-400 hover:text-white hover:border-white/20 transition-all">
          <Filter className="w-4 h-4" />
          Filter
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Total Projects', value: '3', color: 'text-white' },
          { label: 'In Progress', value: '2', color: 'text-[#0099CC]' },
          { label: 'Completed', value: '1', color: 'text-green-400' },
          { label: 'Publications', value: '4', color: 'text-[#FFB300]' },
        ].map(s => (
          <div key={s.label} className="p-4 rounded-xl bg-white/3 border border-white/8 text-center">
            <div className={`text-3xl font-bold ${s.color} mb-1`}>{s.value}</div>
            <div className="text-gray-500 text-xs">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {allProjects.map(project => (
          <Link key={project.id} href={`/projects/${project.id}`}
            className="p-5 rounded-xl bg-white/3 border border-white/8 hover:border-[#0099CC]/30 transition-all group">
            <div className="flex items-start justify-between mb-3">
              <div className="flex flex-wrap gap-1">
                <span className="text-xs px-2 py-0.5 rounded-full bg-[#0099CC]/10 text-[#0099CC] border border-[#0099CC]/20">
                  {project.domain}
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full border ${project.levelStyle}`}>
                  {project.level}
                </span>
              </div>
              <Plane className="w-4 h-4 text-gray-700" />
            </div>

            <h3 className="text-white text-sm font-medium mb-2 line-clamp-2 group-hover:text-[#0099CC] transition-colors">
              {project.title}
            </h3>

            <p className="text-gray-600 text-xs mb-4">{project.theory} • {project.method}</p>

            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>{project.currentStage}</span>
                <span>{project.progress}%</span>
              </div>
              <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-[#0099CC] to-[#003087] transition-all"
                  style={{ width: `${project.progress}%` }}
                />
              </div>
            </div>

            <div className="flex items-center justify-between mt-4 text-xs text-gray-600">
              <span>Updated {project.lastUpdated}</span>
              <div className="flex items-center gap-1 text-[#0099CC] opacity-0 group-hover:opacity-100 transition-opacity">
                <TrendingUp className="w-3 h-3" />
                Open
              </div>
            </div>
          </Link>
        ))}

        {/* New Project Card */}
        <button className="p-5 rounded-xl bg-white/2 border border-dashed border-white/10 hover:border-[#0099CC]/30 hover:bg-[#0099CC]/3 transition-all flex flex-col items-center justify-center gap-3 min-h-[200px] group">
          <div className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-[#0099CC]/10 transition-colors">
            <Plus className="w-6 h-6 text-gray-600 group-hover:text-[#0099CC] transition-colors" />
          </div>
          <div className="text-center">
            <p className="text-gray-500 text-sm group-hover:text-gray-300 transition-colors">Start New Research</p>
            <p className="text-gray-700 text-xs">เริ่มโครงการวิจัยใหม่</p>
          </div>
        </button>
      </div>
    </div>
  )
}

const allProjects = [
  {
    id: '1',
    title: 'AI Adoption and Service Quality in Thai Airlines: A TAM Perspective',
    domain: 'Airline Management',
    level: 'PhD',
    levelStyle: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    theory: 'TAM',
    method: 'SEM',
    progress: 75,
    currentStage: 'Data Analysis',
    lastUpdated: '2h ago',
  },
  {
    id: '2',
    title: 'Digital Transformation and Passenger Satisfaction at Suvarnabhumi Airport',
    domain: 'Airport Management',
    level: "Master's",
    levelStyle: 'bg-green-500/10 text-green-400 border-green-500/20',
    theory: 'UTAUT2',
    method: 'PLS-SEM',
    progress: 45,
    currentStage: 'Framework Design',
    lastUpdated: '1d ago',
  },
  {
    id: '3',
    title: 'Green Logistics and Carbon Reduction in Air Cargo Operations',
    domain: 'Air Cargo',
    level: 'DBA',
    levelStyle: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
    theory: 'RBV',
    method: 'Mixed Methods',
    progress: 30,
    currentStage: 'Literature Review',
    lastUpdated: '3d ago',
  },
]
