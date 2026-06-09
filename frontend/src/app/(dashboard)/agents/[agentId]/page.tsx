'use client'

import { useState, useRef, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { Send, Bot, User, Loader2, Copy, Download, Sparkles, ChevronRight } from 'lucide-react'
import { AGENTS } from '@/lib/constants'
import { cn } from '@/lib/utils'

interface Message {
  id: string
  role: 'user' | 'agent'
  content: string
  timestamp: Date
}

export default function AgentPage() {
  const params = useParams()
  const agentId = params.agentId as string
  const agent = AGENTS.find(a => a.id === agentId)

  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [language, setLanguage] = useState<'th' | 'en'>('th')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (agent) {
      setMessages([{
        id: '1',
        role: 'agent',
        content: language === 'th'
          ? `สวัสดีครับ! ผมคือ **${agent.nameTh}** — ${agent.description}\n\nผมพร้อมช่วยท่านในด้านการวิจัยด้านการบินครับ มีอะไรให้ช่วยไหมครับ? 🛫`
          : `Hello! I'm **${agent.name}** — ${agent.description}\n\nI'm ready to help with your aviation research. How can I assist you today? ✈️`,
        timestamp: new Date(),
      }])
    }
  }, [agent, language])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/agents/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent_id: agentId,
          message: userMessage.content,
          language,
        }),
      })

      let agentContent = ''

      if (response.ok) {
        const data = await response.json()
        agentContent = data.response
      } else {
        agentContent = getDemoResponse(agentId, userMessage.content, language)
      }

      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: agentContent,
        timestamp: new Date(),
      }])
    } catch {
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: getDemoResponse(agentId, userMessage.content, language),
        timestamp: new Date(),
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (!agent) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="text-gray-400">Agent not found: {agentId}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full max-h-[calc(100vh-8rem)] -m-6">
      {/* Agent Header */}
      <div className="px-6 py-4 border-b border-white/5 bg-[#060B18] flex-shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${agent.color} flex items-center justify-center text-2xl`}>
              {agent.icon}
            </div>
            <div>
              <h1 className="text-white font-semibold">{agent.name}</h1>
              <p className="text-gray-500 text-sm">{agent.nameTh}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Language Toggle */}
            <div className="flex rounded-lg border border-white/10 overflow-hidden">
              <button
                onClick={() => setLanguage('th')}
                className={cn(
                  'px-3 py-1.5 text-xs font-medium transition-colors',
                  language === 'th' ? 'bg-[#0099CC] text-white' : 'text-gray-500 hover:text-gray-300'
                )}
              >
                🇹🇭 ภาษาไทย
              </button>
              <button
                onClick={() => setLanguage('en')}
                className={cn(
                  'px-3 py-1.5 text-xs font-medium transition-colors',
                  language === 'en' ? 'bg-[#0099CC] text-white' : 'text-gray-500 hover:text-gray-300'
                )}
              >
                🇬🇧 English
              </button>
            </div>

            <div className="flex items-center gap-1">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-xs text-gray-500">Online</span>
            </div>
          </div>
        </div>

        {/* Capabilities */}
        <div className="flex flex-wrap gap-2 mt-3">
          {agent.capabilities.map(cap => (
            <span key={cap} className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400 border border-white/8">
              {cap}
            </span>
          ))}
        </div>
      </div>

      {/* Suggested Prompts */}
      {messages.length <= 1 && (
        <div className="px-6 py-3 flex-shrink-0">
          <div className="flex flex-wrap gap-2">
            {getSuggestedPrompts(agentId, language).map((prompt, i) => (
              <button
                key={i}
                onClick={() => setInput(prompt)}
                className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-gray-400 hover:text-white hover:border-[#0099CC]/30 transition-all"
              >
                <Sparkles className="w-3 h-3" />
                {prompt.length > 50 ? prompt.slice(0, 47) + '...' : prompt}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={cn('flex gap-3', msg.role === 'user' ? 'justify-end' : 'justify-start')}>
            {msg.role === 'agent' && (
              <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${agent.color} flex items-center justify-center text-sm flex-shrink-0 mt-0.5`}>
                {agent.icon}
              </div>
            )}
            <div className={cn(
              'max-w-2xl rounded-2xl px-4 py-3 text-sm',
              msg.role === 'user'
                ? 'bg-[#0099CC] text-white rounded-tr-sm'
                : 'bg-white/5 border border-white/8 text-gray-200 rounded-tl-sm'
            )}>
              <div className="whitespace-pre-wrap">{msg.content}</div>
              <div className="text-xs opacity-50 mt-1.5 text-right">
                {msg.timestamp.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#0099CC] to-[#003087] flex items-center justify-center flex-shrink-0 mt-0.5">
                <User className="w-4 h-4 text-white" />
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex gap-3">
            <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${agent.color} flex items-center justify-center text-sm flex-shrink-0`}>
              {agent.icon}
            </div>
            <div className="bg-white/5 border border-white/8 rounded-2xl rounded-tl-sm px-4 py-3">
              <div className="flex items-center gap-2 text-gray-500">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-sm">กำลังประมวลผล...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="px-6 py-4 border-t border-white/5 bg-[#060B18] flex-shrink-0">
        <div className="flex gap-3 items-end">
          <div className="flex-1 bg-white/5 border border-white/10 rounded-xl overflow-hidden focus-within:border-[#0099CC]/40 transition-colors">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={language === 'th' ? 'พิมพ์คำถามหรือคำสั่งของคุณ... (Enter เพื่อส่ง)' : 'Type your question or command... (Enter to send)'}
              rows={1}
              className="w-full bg-transparent px-4 py-3 text-sm text-gray-300 placeholder-gray-600 focus:outline-none resize-none"
              style={{ maxHeight: '120px' }}
              onInput={e => {
                const target = e.target as HTMLTextAreaElement
                target.style.height = 'auto'
                target.style.height = `${Math.min(target.scrollHeight, 120)}px`
              }}
            />
          </div>
          <button
            onClick={sendMessage}
            disabled={!input.trim() || isLoading}
            className={cn(
              'p-3 rounded-xl transition-all',
              input.trim() && !isLoading
                ? 'bg-[#0099CC] text-white hover:bg-[#007AA3]'
                : 'bg-white/5 text-gray-600 cursor-not-allowed'
            )}
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        <p className="text-xs text-gray-700 mt-2">
          Shift+Enter สำหรับขึ้นบรรทัดใหม่ • Enter เพื่อส่ง
        </p>
      </div>
    </div>
  )
}

function getDemoResponse(agentId: string, message: string, language: 'th' | 'en'): string {
  const responses: Record<string, Record<string, string>> = {
    'topic-generator': {
      th: `📋 **หัวข้อวิจัยที่แนะนำสำหรับ Aviation Management**\n\n**หัวข้อที่ 1:** ปัจจัยที่ส่งผลต่อการยอมรับเทคโนโลยี AI ในการดำเนินงานสายการบินไทย: การประยุกต์ใช้โมเดล TAM\n- ทฤษฎี: Technology Acceptance Model (TAM)\n- ตัวแปรอิสระ: Perceived Usefulness, Perceived Ease of Use\n- ตัวแปรตาม: AI Adoption Intention\n- วารสารเป้าหมาย: Journal of Air Transport Management (Q1)\n\n**หัวข้อที่ 2:** ความสัมพันธ์ระหว่างคุณภาพบริการดิจิทัลและความพึงพอใจของผู้โดยสาร\n- ทฤษฎี: SERVQUAL Model\n- วารสารเป้าหมาย: Transportation Research Part A (Q1)\n\n💡 **คำแนะนำ:** หัวข้อที่ 1 มีความน่าสนใจสำหรับ PhD/DBA เนื่องจากยังมีช่องว่างงานวิจัยในบริบทของไทย`,
      en: `📋 **Recommended Aviation Research Topics**\n\n**Topic 1:** Factors Influencing AI Technology Adoption in Thai Airline Operations: A TAM Perspective\n- Theory: Technology Acceptance Model (TAM)\n- Independent Variables: Perceived Usefulness, Perceived Ease of Use\n- Dependent Variable: AI Adoption Intention\n- Target Journal: Journal of Air Transport Management (Q1)\n\n**Topic 2:** Digital Service Quality and Passenger Satisfaction at International Airports\n- Theory: SERVQUAL Model\n- Target Journal: Transportation Research Part A (Q1)\n\n💡 **Recommendation:** Topic 1 has strong research gap potential for Thai aviation context.`,
    },
    'thesis-supervisor': {
      th: `👨‍🏫 **ผลการตรวจบท (Thesis Review)**\n\n**สิ่งที่ดี ✅**\n- โครงสร้างบทที่ 1 ชัดเจน\n- วัตถุประสงค์สอดคล้องกับปัญหาวิจัย\n- ทฤษฎีที่เลือกเหมาะสม\n\n**สิ่งที่ต้องปรับปรุง ⚠️**\n1. Background of the Study: ควรเพิ่มข้อมูลสถิติอุตสาหกรรมการบินล่าสุด (2024-2025)\n2. Research Gap: ระบุช่องว่างงานวิจัยให้ชัดเจนกว่านี้\n3. Research Objectives: ควร SMART (Specific, Measurable, Achievable, Relevant, Time-bound)\n4. Theoretical Framework: อธิบาย justification ในการเลือกทฤษฎีเพิ่มเติม\n\n**คะแนนโดยรวม: 72/100**\n\n🔄 แนะนำให้ปรับปรุงและส่งกลับมาตรวจใหม่ครับ`,
      en: `👨‍🏫 **Thesis Chapter Review**\n\n**Strengths ✅**\n- Clear Chapter 1 structure\n- Objectives align with research problem\n- Appropriate theory selection\n\n**Areas for Improvement ⚠️**\n1. Background: Add recent aviation industry statistics (2024-2025)\n2. Research Gap: Be more specific about the identified gap\n3. Objectives: Make them SMART\n4. Framework: Provide stronger justification for theory selection\n\n**Overall Score: 72/100**\n\n🔄 Please revise and resubmit for review.`,
    },
    'sem-expert': {
      th: `🔬 **ผลการตรวจสอบ CFA/SEM Model**\n\n**Model Fit Indices:**\n| Index | Value | Criterion | Status |\n|-------|-------|-----------|--------|\n| χ²/df | 2.134 | < 3.0 | ✅ ดี |\n| CFI | 0.967 | > 0.95 | ✅ ดีมาก |\n| TLI | 0.961 | > 0.95 | ✅ ดีมาก |\n| RMSEA | 0.043 | < 0.08 | ✅ ดี |\n| SRMR | 0.051 | < 0.08 | ✅ ดี |\n\n**Construct Validity:**\n- CR (Composite Reliability): 0.87 > 0.70 ✅\n- AVE (Average Variance Extracted): 0.62 > 0.50 ✅\n- HTMT: 0.76 < 0.85 ✅\n\n**สรุป:** โมเดลมีความเหมาะสมดีและสามารถรายงานผลได้ครับ 🎉`,
      en: `🔬 **CFA/SEM Model Assessment**\n\n**Model Fit Indices:**\n| Index | Value | Criterion | Status |\n|-------|-------|-----------|--------|\n| χ²/df | 2.134 | < 3.0 | ✅ Good |\n| CFI | 0.967 | > 0.95 | ✅ Excellent |\n| TLI | 0.961 | > 0.95 | ✅ Excellent |\n| RMSEA | 0.043 | < 0.08 | ✅ Good |\n| SRMR | 0.051 | < 0.08 | ✅ Good |\n\n**Construct Validity:**\n- CR: 0.87 > 0.70 ✅\n- AVE: 0.62 > 0.50 ✅\n- HTMT: 0.76 < 0.85 ✅\n\n**Conclusion:** Model demonstrates good fit. Ready to report! 🎉`,
    },
  }

  const agentResponses = responses[agentId]
  if (agentResponses) {
    return agentResponses[language] || agentResponses['en']
  }

  return language === 'th'
    ? `ขอบคุณสำหรับคำถามครับ! ผมกำลังประมวลผลข้อมูลเกี่ยวกับ "${message.slice(0, 50)}..." \n\nกรุณาตั้งค่า API Key ใน .env เพื่อเปิดใช้งานการตอบสนองแบบ AI จริงครับ\n\n🔧 **DEMO MODE** — กำลังแสดงผลตัวอย่าง`
    : `Thank you for your question! Processing your request about "${message.slice(0, 50)}..."\n\nPlease configure your API Key in .env to enable real AI responses.\n\n🔧 **DEMO MODE** — Showing sample response`
}

function getSuggestedPrompts(agentId: string, language: 'th' | 'en'): string[] {
  const prompts: Record<string, Record<string, string[]>> = {
    'topic-generator': {
      th: [
        'สร้างหัวข้อวิจัย PhD ด้าน Airline Management ที่ตีพิมพ์ใน Q1 ได้',
        'หัวข้อ DBA เกี่ยวกับ Digital Transformation ที่สนามบิน',
        'ช่องว่างงานวิจัยด้าน Aviation Safety ที่ยังไม่มีคนทำ',
      ],
      en: [
        'Generate PhD research topics on Airline Management for Q1 journals',
        'Research gaps in Airport Digital Transformation',
        'Suggest DBA research topics on Air Cargo sustainability',
      ],
    },
    'thesis-supervisor': {
      th: [
        'ตรวจสอบบทที่ 1 ของฉัน: หัวข้อ "ปัจจัยที่ส่งผลต่อความพึงพอใจผู้โดยสาร"',
        'ช่วยตรวจสอบความสอดคล้องของวัตถุประสงค์กับสมมติฐาน',
        'ให้ feedback บทที่ 3 ระเบียบวิธีวิจัย',
      ],
      en: [
        'Review my Chapter 1 on passenger satisfaction in aviation',
        'Check alignment between objectives and hypotheses',
        'Give feedback on my research methodology chapter',
      ],
    },
    'sem-expert': {
      th: [
        'ตรวจสอบ CFA model ของฉัน: CFI=0.95, RMSEA=0.05',
        'อธิบายวิธีแก้ไขเมื่อ model fit ไม่ดี',
        'วิธีรายงานผล SEM ใน APA format',
      ],
      en: [
        'Check my CFA model: CFI=0.95, RMSEA=0.05',
        'How to fix poor model fit in SEM',
        'How to report SEM results in APA format',
      ],
    },
  }

  return prompts[agentId]?.[language] || (language === 'th'
    ? ['ถามคำถามที่เกี่ยวข้องกับการวิจัยด้านการบิน', 'ขอความช่วยเหลือด้านงานวิจัย', 'สร้างเนื้อหาวิชาการ']
    : ['Ask a question about aviation research', 'Get help with your research', 'Generate academic content']
  )
}
