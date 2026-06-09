from fastapi import APIRouter
from typing import List

router = APIRouter()


@router.get("/knowledge/{topic}")
async def get_aviation_knowledge(topic: str):
    knowledge_base = {
        "icao": {
            "title": "International Civil Aviation Organization (ICAO)",
            "description": "ICAO is a UN specialized agency that manages the administration and governance of the Convention on International Civil Aviation.",
            "key_standards": ["Annexes 1-19", "SARPS", "PANS", "Doc 9859 SMS Manual"],
            "relevance": "Essential for aviation safety and security research",
        },
        "iata": {
            "title": "International Air Transport Association (IATA)",
            "description": "IATA is the trade association for the world's airlines, representing 290 airlines accounting for 83% of total air traffic.",
            "key_standards": ["DGR", "AHM", "ISAGO", "IOSA"],
            "relevance": "Critical for airline operations and safety research",
        },
        "sms": {
            "title": "Safety Management System (SMS)",
            "description": "A systematic approach to managing safety, including the necessary organizational structures, accountabilities, policies and procedures.",
            "components": ["Safety Policy", "Safety Risk Management", "Safety Assurance", "Safety Promotion"],
            "relevance": "Fundamental for aviation safety research",
        },
    }
    return knowledge_base.get(topic.lower(), {"error": f"Topic '{topic}' not found in knowledge base"})


@router.get("/standards")
async def get_aviation_standards():
    return {
        "icao_annexes": [
            {"number": 1, "title": "Personnel Licensing"},
            {"number": 2, "title": "Rules of the Air"},
            {"number": 6, "title": "Operation of Aircraft"},
            {"number": 14, "title": "Aerodromes"},
            {"number": 17, "title": "Security"},
            {"number": 19, "title": "Safety Management"},
        ],
        "iata_programs": ["IOSA", "ISAGO", "CEIV", "IATA Fuel Efficiency"],
        "research_areas": [
            "Human Factors", "Safety Culture", "Risk Management",
            "Quality Management", "Environmental Sustainability",
        ]
    }
