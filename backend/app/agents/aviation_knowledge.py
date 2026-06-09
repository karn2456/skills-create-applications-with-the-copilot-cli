from app.agents.base_agent import BaseAgent
from typing import Any, Dict, Optional


class AviationKnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__("aviation-knowledge", "Aviation Knowledge Agent")

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        message = input_data.get("message", "")
        language = input_data.get("language", "th")

        system_prompt = """You are an expert Aviation Knowledge specialist with deep expertise in:
- ICAO Standards and Recommended Practices (SARPs), Annexes 1-19
- IATA DGR, AHM, ISAGO, IOSA programs
- Airport Management (ICAO Doc 9137, ADRM)
- Air Cargo Management and IATA regulations
- Aviation Safety Management (SMS, Doc 9859)
- Air Traffic Management and SESAR/NextGen
- Airline Operations and Revenue Management
- Aviation Law and Regulations
- Thailand Civil Aviation Authority (CAAT) regulations
Provide accurate, regulation-referenced information for aviation research."""

        response = await self.get_llm_response(
            f"Aviation knowledge query: {message} (Language: {language})",
            system_prompt
        )

        return {
            "response": response,
            "suggestions": ["Cross-reference with ICAO documents", "Check for recent amendments"],
            "next_steps": ["Apply knowledge to research", "Cite regulatory sources"],
        }
