from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.research import AgentChatRequest, AgentChatResponse
from app.agents.orchestrator import AgentOrchestrator
from typing import List

router = APIRouter()
orchestrator = AgentOrchestrator()

AVAILABLE_AGENTS = [
    {"id": "topic-generator", "name": "Research Topic Generator", "status": "active"},
    {"id": "literature-review", "name": "Literature Review Agent", "status": "active"},
    {"id": "citation-mapping", "name": "Citation Mapping Agent", "status": "active"},
    {"id": "research-gap", "name": "Research Gap Agent", "status": "active"},
    {"id": "framework-builder", "name": "Conceptual Framework Agent", "status": "active"},
    {"id": "questionnaire", "name": "Questionnaire Builder", "status": "active"},
    {"id": "data-analysis", "name": "Data Analysis Agent", "status": "active"},
    {"id": "paper-writing", "name": "Paper Writing Agent", "status": "active"},
    {"id": "publication", "name": "Publication Agent", "status": "active"},
    {"id": "thesis-supervisor", "name": "Thesis Supervisor Agent", "status": "active"},
    {"id": "sem-expert", "name": "SEM/CFA Expert Agent", "status": "active"},
    {"id": "aviation-knowledge", "name": "Aviation Knowledge Agent", "status": "active"},
]


@router.get("/", response_model=List[dict])
async def list_agents():
    return AVAILABLE_AGENTS


@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    agent = next((a for a in AVAILABLE_AGENTS if a["id"] == agent_id), None)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.post("/chat", response_model=AgentChatResponse)
async def chat_with_agent(request: AgentChatRequest):
    try:
        response = await orchestrator.process_message(
            agent_id=request.agent_id,
            message=request.message,
            context=request.context,
            language=request.language,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
