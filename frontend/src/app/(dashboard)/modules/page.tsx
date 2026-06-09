import { Plane, Package, Building2, Shield, Cpu, Leaf, Users, TrendingUp, ArrowRight, BookOpen } from 'lucide-react'
import Link from 'next/link'

export default function ModulesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Aviation Domain Modules</h1>
        <p className="text-gray-500 text-sm mt-1">
          โมดูลความรู้เฉพาะด้านการบิน — Deep domain knowledge for aviation research
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {modules.map(mod => (
          <div key={mod.id} className="p-5 rounded-xl bg-white/3 border border-white/8 hover:border-white/15 transition-all group">
            <div className="flex items-start gap-4 mb-4">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${mod.gradient} flex items-center justify-center flex-shrink-0`}>
                <mod.icon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-white font-semibold">{mod.name}</h3>
                <p className="text-gray-500 text-xs mt-0.5">{mod.nameTh}</p>
              </div>
            </div>

            <p className="text-gray-400 text-sm mb-4">{mod.description}</p>

            <div className="flex flex-wrap gap-1 mb-4">
              {mod.tags.map(tag => (
                <span key={tag} className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-500 border border-white/8">
                  {tag}
                </span>
              ))}
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4 text-xs text-gray-600">
                <span className="flex items-center gap-1">
                  <BookOpen className="w-3 h-3" />
                  {mod.topics} topics
                </span>
                <span className="flex items-center gap-1">
                  <TrendingUp className="w-3 h-3" />
                  {mod.papers} papers
                </span>
              </div>
              <Link href={`/agents/topic-generator?domain=${mod.id}`}
                className="flex items-center gap-1 text-xs text-[#0099CC] hover:text-[#00B4D8] transition-colors opacity-0 group-hover:opacity-100">
                Explore <ArrowRight className="w-3 h-3" />
              </Link>
            </div>
          </div>
        ))}
      </div>

      {/* ICAO/IATA Standards */}
      <div className="mt-8">
        <h2 className="text-white font-semibold mb-4">Aviation Standards & Regulations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-5 rounded-xl bg-gradient-to-br from-[#003087]/20 to-transparent border border-[#003087]/20">
            <h3 className="text-white font-medium mb-3">🌐 ICAO Standards</h3>
            <div className="space-y-2">
              {icaoAnnexes.map(annex => (
                <div key={annex.number} className="flex items-center gap-3 text-sm">
                  <span className="text-[#0099CC] w-16 flex-shrink-0">Annex {annex.number}</span>
                  <span className="text-gray-400">{annex.title}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="p-5 rounded-xl bg-gradient-to-br from-[#FFB300]/10 to-transparent border border-[#FFB300]/15">
            <h3 className="text-white font-medium mb-3">✈️ IATA Programs</h3>
            <div className="space-y-2">
              {iataPrograms.map(prog => (
                <div key={prog.id} className="flex items-start gap-3 text-sm">
                  <span className="text-[#FFB300] w-16 flex-shrink-0 font-medium">{prog.id}</span>
                  <span className="text-gray-400">{prog.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

const modules = [
  {
    id: 'airline',
    name: 'Airline Management',
    nameTh: 'การจัดการสายการบิน',
    icon: Plane,
    gradient: 'from-blue-500 to-cyan-600',
    description: 'Airline business strategy, revenue management, operations, and digital transformation',
    tags: ['Revenue Management', 'Digital', 'Operations', 'Strategy'],
    topics: 245,
    papers: 1240,
  },
  {
    id: 'airport',
    name: 'Airport Management',
    nameTh: 'การจัดการท่าอากาศยาน',
    icon: Building2,
    gradient: 'from-purple-500 to-indigo-600',
    description: 'Airport operations, capacity management, smart airport technology, and passenger experience',
    tags: ['Smart Airport', 'Capacity', 'Passenger', 'IoT'],
    topics: 189,
    papers: 890,
  },
  {
    id: 'cargo',
    name: 'Air Cargo & Logistics',
    nameTh: 'การขนส่งสินค้าทางอากาศ',
    icon: Package,
    gradient: 'from-orange-500 to-amber-600',
    description: 'Air freight operations, e-commerce logistics, cold chain, and supply chain management',
    tags: ['E-commerce', 'Cold Chain', 'Supply Chain', 'Sustainability'],
    topics: 156,
    papers: 678,
  },
  {
    id: 'safety',
    name: 'Aviation Safety',
    nameTh: 'ความปลอดภัยการบิน',
    icon: Shield,
    gradient: 'from-red-500 to-rose-600',
    description: 'Safety Management System (SMS), human factors, risk management, and safety culture',
    tags: ['SMS', 'Human Factors', 'Risk', 'Safety Culture'],
    topics: 201,
    papers: 1120,
  },
  {
    id: 'technology',
    name: 'Aviation Technology',
    nameTh: 'เทคโนโลยีการบิน',
    icon: Cpu,
    gradient: 'from-teal-500 to-green-600',
    description: 'AI, IoT, blockchain, digital twins, and emerging technologies in aviation',
    tags: ['AI', 'IoT', 'Blockchain', 'Digital Twin'],
    topics: 178,
    papers: 892,
  },
  {
    id: 'sustainability',
    name: 'Aviation Sustainability',
    nameTh: 'ความยั่งยืนด้านการบิน',
    icon: Leaf,
    gradient: 'from-green-500 to-emerald-600',
    description: 'SAF, carbon reduction, ESG, net-zero aviation, and environmental management',
    tags: ['SAF', 'Carbon', 'ESG', 'Net Zero'],
    topics: 134,
    papers: 567,
  },
  {
    id: 'passenger',
    name: 'Passenger Experience',
    nameTh: 'ประสบการณ์ผู้โดยสาร',
    icon: Users,
    gradient: 'from-pink-500 to-rose-600',
    description: 'Passenger satisfaction, service quality, loyalty, and CX in aviation',
    tags: ['Satisfaction', 'Loyalty', 'Service Quality', 'CX'],
    topics: 167,
    papers: 834,
  },
  {
    id: 'economics',
    name: 'Air Transport Economics',
    nameTh: 'เศรษฐศาสตร์การขนส่งทางอากาศ',
    icon: TrendingUp,
    gradient: 'from-sky-500 to-blue-600',
    description: 'Airline economics, pricing, market analysis, deregulation, and post-COVID recovery',
    tags: ['Pricing', 'Market Analysis', 'Deregulation', 'Recovery'],
    topics: 143,
    papers: 712,
  },
]

const icaoAnnexes = [
  { number: 1, title: 'Personnel Licensing' },
  { number: 6, title: 'Operation of Aircraft' },
  { number: 9, title: 'Facilitation' },
  { number: 14, title: 'Aerodromes' },
  { number: 17, title: 'Security (AVSEC)' },
  { number: 19, title: 'Safety Management' },
]

const iataPrograms = [
  { id: 'IOSA', name: 'IATA Operational Safety Audit' },
  { id: 'ISAGO', name: 'IATA Safety Audit for Ground Operations' },
  { id: 'CEIV', name: 'Center of Excellence for Independent Validators' },
  { id: 'DGR', name: 'Dangerous Goods Regulations' },
  { id: 'AHM', name: 'Airport Handling Manual' },
]
