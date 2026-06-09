# ✈️ AROS — Aviation Research Operating System

> The First AI-Native Research Platform for Aviation Management

![AROS Banner](./images/aros-banner.png)

## Overview

AROS (Aviation Research Operating System) is a comprehensive AI-powered research platform designed specifically for:

- ✈️ **Aviation Management** research
- 🏢 **Airport Management** studies  
- 📦 **Air Cargo & Logistics** research
- 🛡️ **Aviation Safety** investigations
- 🎓 **Master's Thesis** (ป.โท)
- 🔬 **PhD Dissertations** (ป.เอก)
- 💼 **DBA Research**

Inspired by Orchestra Research but purpose-built for the aviation domain.

---

## 🤖 12 Specialized AI Agents

| Agent | Function |
|-------|----------|
| 🎯 Topic Generator | Generate novel aviation research topics |
| 📚 Literature Review | Search Scopus, WoS, Semantic Scholar |
| 🕸️ Citation Mapping | Build citation graphs & bibliometrics |
| 🔍 Research Gap | Detect underexplored research areas |
| 🏗️ Framework Builder | Design TAM, UTAUT, SERVQUAL frameworks |
| 📋 Questionnaire Builder | Generate bilingual Thai-English questionnaires |
| 📊 Data Analysis | SEM, CFA, PLS-SEM, APA-style reports |
| ✍️ Paper Writing | Complete thesis chapters 1-5 + Scopus papers |
| 📰 Publication Agent | Journal matching, cover letters |
| 👨‍🏫 Thesis Supervisor | AI advisor-level thesis review |
| 🔬 SEM/CFA Expert | CR, AVE, HTMT validation specialist |
| ✈️ Aviation Knowledge | ICAO, IATA, aviation standards expert |

---

## 🏗️ Architecture

```
AROS/
├── frontend/          # Next.js 14 + TypeScript + TailwindCSS
│   ├── src/app/       # Next.js App Router
│   ├── src/components/ # React Components
│   └── src/lib/       # Utilities & Constants
├── backend/           # Python FastAPI
│   ├── app/agents/    # 12 AI Agents
│   ├── app/routers/   # API Endpoints
│   └── app/models/    # Pydantic Models
└── docker-compose.yml # Full stack deployment
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- Docker (optional)

### Frontend
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
uvicorn main:app --reload
# API docs: http://localhost:8000/docs
```

### Docker (Full Stack)
```bash
docker-compose up -d
```

---

## 🔑 API Keys Required

Add to `backend/.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

---

## 📚 Research Workflow

```
Topic Generation → Literature Review → Gap Detection → Framework Design
→ Questionnaire → Data Collection → Statistical Analysis → Paper Writing → Publication
```

---

## ✈️ Aviation Modules

- Airline Management (245+ research topics)
- Airport Management (189+ topics)
- Air Cargo & Logistics (156+ topics)
- Aviation Safety (201+ topics)
- Aviation Technology (178+ topics)
- Aviation Sustainability (134+ topics)
- Passenger Experience (167+ topics)
- Air Transport Economics (143+ topics)

---

## 🎓 For Thai Aviation Researchers

AROS is designed for:
- **CATC** (Civil Aviation Training Center)
- **Kasetsart University** Aviation Management
- **Mahidol University** ICIT
- **Bangkok University** Aviation programs
- **Rangsit University** Aviation

Supporting both Thai and English language outputs.

---

## 📊 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, TypeScript, TailwindCSS, ShadCN UI |
| Backend | Python FastAPI |
| AI Layer | Claude (Anthropic), GPT-4o (OpenAI) |
| Agent Framework | LangGraph |
| Vector DB | Qdrant |
| Database | PostgreSQL |
| Cache | Redis |
| Deployment | Docker, Kubernetes |

---

## 📄 License

MIT License — Built for advancing aviation research

---

*AROS — Advancing Aviation Research with AI* ✈️🔬
