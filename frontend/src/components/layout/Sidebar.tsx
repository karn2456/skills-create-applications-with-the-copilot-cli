'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard, Plane, BookOpen, Network, Search,
  Grid, FileQuestion, BarChart3, FileText, Send,
  GraduationCap, FlaskConical, Database, Settings,
  ChevronRight, Sparkles
} from 'lucide-react'

const navigation = [
  {
    group: 'Overview',
    items: [
      { id: 'dashboard', label: 'Dashboard', labelTh: 'แดชบอร์ด', href: '/dashboard', icon: LayoutDashboard },
      { id: 'projects', label: 'My Projects', labelTh: 'โครงการวิจัย', href: '/projects', icon: Grid },
    ]
  },
  {
    group: 'AI Agents',
    groupTh: 'AI Agents',
    items: [
      { id: 'topic', label: 'Topic Generator', labelTh: 'สร้างหัวข้อวิจัย', href: '/agents/topic-generator', icon: Sparkles },
      { id: 'literature', label: 'Literature Review', labelTh: 'ทบทวนวรรณกรรม', href: '/agents/literature-review', icon: BookOpen },
      { id: 'citation', label: 'Citation Mapping', labelTh: 'แผนที่การอ้างอิง', href: '/agents/citation-mapping', icon: Network },
      { id: 'gap', label: 'Research Gap', labelTh: 'ช่องว่างงานวิจัย', href: '/agents/research-gap', icon: Search },
      { id: 'framework', label: 'Framework Builder', labelTh: 'กรอบแนวคิด', href: '/agents/framework-builder', icon: Grid },
      { id: 'questionnaire', label: 'Questionnaire', labelTh: 'แบบสอบถาม', href: '/agents/questionnaire', icon: FileQuestion },
      { id: 'analysis', label: 'Data Analysis', labelTh: 'วิเคราะห์ข้อมูล', href: '/agents/data-analysis', icon: BarChart3 },
      { id: 'writing', label: 'Paper Writing', labelTh: 'เขียนบทความ', href: '/agents/paper-writing', icon: FileText },
      { id: 'publication', label: 'Publication', labelTh: 'ตีพิมพ์', href: '/agents/publication', icon: Send },
    ]
  },
  {
    group: 'Special Agents',
    groupTh: 'Agents พิเศษ',
    items: [
      { id: 'thesis', label: 'Thesis Supervisor', labelTh: 'อ.ที่ปรึกษา AI', href: '/agents/thesis-supervisor', icon: GraduationCap },
      { id: 'sem', label: 'SEM/CFA Expert', labelTh: 'ผู้เชี่ยวชาญ SEM', href: '/agents/sem-expert', icon: FlaskConical },
      { id: 'aviation', label: 'Aviation Knowledge', labelTh: 'ความรู้การบิน', href: '/agents/aviation-knowledge', icon: Plane },
    ]
  },
  {
    group: 'Aviation Modules',
    items: [
      { id: 'modules', label: 'Domain Modules', labelTh: 'โมดูลด้านการบิน', href: '/modules', icon: Database },
    ]
  },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="w-64 bg-[#060B18] border-r border-white/5 flex flex-col h-full overflow-y-auto">
      {/* Logo */}
      <div className="px-5 py-5 border-b border-white/5">
        <Link href="/" className="flex items-center gap-3">
          <div className="w-9 h-9 bg-gradient-to-br from-[#0099CC] to-[#003087] rounded-lg flex items-center justify-center">
            <Plane className="w-5 h-5 text-white" />
          </div>
          <div>
            <span className="font-bold text-white text-base">AROS</span>
            <p className="text-[10px] text-[#0099CC] leading-none">Aviation Research OS</p>
          </div>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-6">
        {navigation.map((group) => (
          <div key={group.group}>
            <p className="text-[10px] font-semibold text-gray-600 uppercase tracking-wider px-3 mb-2">
              {group.group}
            </p>
            <div className="space-y-0.5">
              {group.items.map((item) => {
                const isActive = pathname === item.href
                return (
                  <Link
                    key={item.id}
                    href={item.href}
                    className={cn(
                      'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all group',
                      isActive
                        ? 'bg-[#0099CC]/10 text-[#0099CC] border border-[#0099CC]/20'
                        : 'text-gray-500 hover:text-gray-300 hover:bg-white/5'
                    )}
                  >
                    <item.icon className={cn(
                      'w-4 h-4 flex-shrink-0',
                      isActive ? 'text-[#0099CC]' : 'text-gray-600 group-hover:text-gray-400'
                    )} />
                    <div className="flex-1 min-w-0">
                      <div className="truncate">{item.label}</div>
                      {item.labelTh && (
                        <div className="text-[10px] truncate opacity-60">{item.labelTh}</div>
                      )}
                    </div>
                    {isActive && <ChevronRight className="w-3 h-3 flex-shrink-0" />}
                  </Link>
                )
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* Bottom */}
      <div className="px-3 py-4 border-t border-white/5">
        <Link href="/settings" className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-gray-500 hover:text-gray-300 hover:bg-white/5 transition-all">
          <Settings className="w-4 h-4" />
          Settings
        </Link>
        <div className="mt-3 p-3 rounded-lg bg-gradient-to-br from-[#003087]/30 to-[#0099CC]/10 border border-[#0099CC]/10">
          <p className="text-xs text-[#0099CC] font-medium mb-1">✈️ Aviation Research Mode</p>
          <p className="text-[10px] text-gray-500">AI-powered research for aviation management</p>
        </div>
      </div>
    </div>
  )
}
