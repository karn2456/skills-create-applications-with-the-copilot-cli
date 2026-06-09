from fastapi import APIRouter, HTTPException
from app.models.research import TopicGenerationRequest, TopicGenerationResponse
from app.agents.topic_generator import TopicGeneratorAgent
from typing import List

router = APIRouter()
topic_agent = TopicGeneratorAgent()


@router.post("/topics/generate", response_model=TopicGenerationResponse)
async def generate_topics(request: TopicGenerationRequest):
    try:
        return await topic_agent.generate(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/domains")
async def get_aviation_domains():
    return [
        {"id": "airline", "name": "Airline Management", "topics_count": 245},
        {"id": "airport", "name": "Airport Management", "topics_count": 189},
        {"id": "cargo", "name": "Air Cargo & Logistics", "topics_count": 156},
        {"id": "safety", "name": "Aviation Safety", "topics_count": 201},
        {"id": "technology", "name": "Aviation Technology", "topics_count": 178},
        {"id": "sustainability", "name": "Aviation Sustainability", "topics_count": 134},
        {"id": "passenger", "name": "Passenger Experience", "topics_count": 167},
        {"id": "economics", "name": "Air Transport Economics", "topics_count": 143},
    ]


@router.get("/frameworks")
async def get_research_frameworks():
    return [
        {"id": "tam", "name": "Technology Acceptance Model (TAM)", "domain": "technology"},
        {"id": "utaut", "name": "UTAUT", "domain": "technology"},
        {"id": "servqual", "name": "SERVQUAL", "domain": "service"},
        {"id": "ect", "name": "Expectation Confirmation Theory", "domain": "satisfaction"},
        {"id": "rbv", "name": "Resource-Based View", "domain": "strategy"},
        {"id": "toe", "name": "TOE Framework", "domain": "adoption"},
    ]
