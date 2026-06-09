# Orchestra Research ARA vs GitLab Duo Agent Platform
## Technical Architecture Deep-Dive & Comparison

---

## 1. Orchestra Research ARA — Architecture Analysis

### Core Concept
Orchestra เป็น **"First AI-Native Research IDE"** ที่ออกแบบมาสำหรับ open-ended, long-horizon research workflows โดยเน้น **Human-in-the-Loop + Agent Execution**

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER / RESEARCHER                            │
│              (propose hypothesis, curate, supervise)            │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│              RESEARCH COMPANION (Orchestrator)                  │
│   • Routes research tasks to specialized agents                 │
│   • Maintains long-horizon session state                        │
│   • Preserves "research taste" personalization                  │
└──────────┬──────────────────┬───────────────────┬───────────────┘
           │                  │                   │
┌──────────▼──────┐  ┌────────▼────────┐  ┌──────▼──────────────┐
│  COGNITIVE      │  │  ENGINEERING    │  │  INFRASTRUCTURE     │
│  LAYER          │  │  LAYER          │  │  LAYER              │
│                 │  │                 │  │                     │
│ • Domain Expert │  │ • Code Gen      │  │ • Total Recall      │
│ • Hypothesis    │  │ • Env Setup     │  │   (Long-horizon     │
│   Design        │  │ • Dependency    │  │    Memory Store)    │
│ • Experiment    │  │   Manager       │  │ • Context Engine    │
│   Planning      │  │ • GPU Monitor   │  │ • Compute Manager   │
│ • Result        │  │ • Execution     │  │ • Dead-end Index    │
│   Interpretation│  │   Engine        │  │ • Research Graph    │
└─────────────────┘  └─────────────────┘  └─────────────────────┘
```

### Research Workflow (Agent Pipeline)

```
Reading → Querying → Generation → Curation → Execution → Supervision
   │           │           │           │           │           │
   ▼           ▼           ▼           ▼           ▼           ▼
Literature  AI Q&A    Hypothesis  Human        Agent       Human
 Review    on Papers   Generator  Selects    Executes    Reviews
  Agent    Interface              Direction  Experiments  Results
```

### Key Technical Characteristics
| Feature | Detail |
|---------|--------|
| Memory Type | **Total Recall** — persistent, indexed, long-horizon (weeks/months) |
| Agent Pattern | Supervisor-Worker (Human supervisor + AI agents) |
| State | Long-horizon stateful sessions with dead-end tracking |
| Specialization | Research domain: NLP, CV, Systems, Theory |
| Workflow | Open-ended discovery loops (not linear pipelines) |
| Human Role | Curate direction + supervise execution |
| Agent Role | Execute everything between propose & result |

---

## 2. GitLab Duo Agent Platform — Architecture

### Core Concept
GitLab Duo ใช้ **Task-Routing Orchestrator** ที่ส่งต่องาน DevOps ไปยัง Specialized Agents ที่มี Tools ต่างกัน

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER / DEVELOPER                             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                  DUO CHAT (Orchestrator)                        │
│   Intent Classification → Task Routing → Response Synthesis     │
└──────┬──────────┬───────────┬───────────┬────────────┬──────────┘
       │          │           │           │            │
┌──────▼──┐  ┌───▼───┐  ┌───▼────┐  ┌──▼──────┐  ┌──▼──────┐
│Planning │  │ Code  │  │Review  │  │Security │  │  Docs   │
│  Agent  │  │ Agent │  │ Agent  │  │  Agent  │  │  Agent  │
│         │  │       │  │        │  │         │  │         │
│Task     │  │Gen,   │  │PR      │  │SAST,    │  │Generate │
│Breakdown│  │Complete│ │Review, │  │Secrets, │  │Explain, │
│Sprint   │  │Explain│  │Suggest │  │Deps     │  │Search   │
└────┬────┘  └───┬───┘  └───┬────┘  └──┬──────┘  └──┬──────┘
     │           │          │           │             │
┌────▼───────────▼──────────▼───────────▼─────────────▼──────────┐
│                        TOOL REGISTRY                            │
│  IDE Tools │ Git Tools │ CI/CD Tools │ Search │ External APIs   │
└─────────────────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                    CONTEXT / MEMORY LAYER                       │
│   Repository Context │ User Preferences │ Session History       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Side-by-Side Comparison

| Dimension | Orchestra Research ARA | GitLab Duo Agent Platform |
|-----------|----------------------|--------------------------|
| **Domain** | Open-ended Scientific Research | DevOps / Software Engineering |
| **Orchestrator** | Research Companion | Duo Chat |
| **Architecture Pattern** | Three-Layer (Cognitive/Engineering/Infra) | Task-Router + Specialized Agents |
| **Memory** | Total Recall (persistent, long-horizon, months) | Session context + Repository context |
| **Human Role** | Propose + Curate + Supervise | Issue task + Approve |
| **Agent Execution** | Agents handle all execution between hypothesis & result | Agents handle code gen, review, security |
| **Tool Use** | GPU compute, code execution, experiment runner | IDE, Git, CI/CD, search APIs |
| **State Management** | Long-horizon stateful (dead-end tracking, research graph) | Per-session + repo state |
| **Multi-Agent** | Yes — Literature, Experiment, Analysis agents | Yes — Code, Review, Security, Docs agents |
| **Personalization** | Research taste & philosophy over time | User preferences, project context |
| **Open-ended** | Yes — designed for divergent exploration | Partial — task-completion focused |

### Verdict: Same Pattern, Different Domain

**คำตอบ: ใช่ — Orchestra Research ARA ใช้สถาปัตยกรรมแบบเดียวกับ GitLab Duo Agent Platform**

ทั้งสองระบบ share fundamental agent platform pattern:
1. **Central Orchestrator** → routes tasks to specialized agents
2. **Specialized Sub-Agents** → each with domain tools & expertise  
3. **Persistent Memory/Context** → spans across sessions
4. **Human-in-the-Loop** → supervision gates at key decision points
5. **Tool Registry** → external tool integration per agent
6. **Layered Architecture** → presentation / reasoning / infrastructure

ความแตกต่างหลักคือ **domain** และ **memory horizon**:
- Orchestra: Research domain + weeks/months memory (Total Recall)
- GitLab Duo: DevOps domain + session/repo memory

---

## 4. Aviation Research Agent Platform — Extension Design

### Proposed Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│              AVIATION RESEARCH ORCHESTRATOR                      │
│          (Research Companion — adapted from Orchestra)           │
└──┬────────────┬───────────────┬──────────┬──────────┬────────────┘
   │            │               │          │          │
┌──▼──────┐  ┌─▼──────────┐  ┌─▼──────┐  ┌▼──────┐  ┌▼────────────┐
│Literature│  │Questionnaire│  │  SEM   │  │  APA  │  │  Thesis     │
│ Review  │  │  Design    │  │Analysis│  │Referen│  │  Reviewer   │
│  Agent  │  │   Agent    │  │ Agent  │  │ Agent │  │   Agent     │
└──────────┘  └────────────┘  └────────┘  └───────┘  └─────────────┘
```

See `aviation_research_platform/` for full implementation.
