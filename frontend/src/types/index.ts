export interface Agent {
  id: string
  name: string
  nameTh: string
  description: string
  icon: string
  color: string
  capabilities: string[]
  category: string
}

export interface ResearchProject {
  id: string
  title: string
  titleTh?: string
  domain: string
  status: 'ideation' | 'literature' | 'framework' | 'questionnaire' | 'data-collection' | 'analysis' | 'writing' | 'publication'
  progress: number
  createdAt: string
  updatedAt: string
  agentHistory: AgentSession[]
}

export interface AgentSession {
  agentId: string
  timestamp: string
  input: string
  output: string
  status: 'completed' | 'pending' | 'error'
}

export interface LiteratureSource {
  id: string
  title: string
  authors: string[]
  year: number
  journal: string
  doi?: string
  abstract: string
  citations: number
  relevanceScore: number
  tags: string[]
}

export interface ResearchGap {
  id: string
  area: string
  description: string
  opportunity: string
  relatedTopics: string[]
  priority: 'high' | 'medium' | 'low'
}

export interface ConceptualFramework {
  id: string
  title: string
  theory: string
  variables: {
    independent: string[]
    dependent: string[]
    mediating: string[]
    moderating: string[]
  }
  hypotheses: string[]
  diagramUrl?: string
}

export interface AgentMessage {
  id: string
  role: 'user' | 'agent'
  content: string
  timestamp: string
  agentId?: string
  attachments?: string[]
}

export interface DashboardStats {
  totalProjects: number
  activeResearch: number
  papersGenerated: number
  citationsAnalyzed: number
  questionnairesCreated: number
  avgResearchProgress: number
}
