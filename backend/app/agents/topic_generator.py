from app.agents.base_agent import BaseAgent
from app.models.research import TopicGenerationRequest, TopicGenerationResponse
from typing import Any, Dict, Optional


class TopicGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("topic-generator", "Research Topic Generator")
        self.system_prompt = """You are an expert Aviation Research Topic Generator specialized in:
- Aviation Management, Air Transport, Airline Business
- Airport Management, Air Cargo, Logistics
- Aviation Safety, Aviation Technology, Sustainability
- Master's Thesis, PhD Dissertation, DBA Research

Generate research topics that are:
1. Novel and publishable in Scopus Q1/Q2 journals
2. Aligned with current aviation industry challenges
3. Suitable for quantitative research with SEM/CFA methodology
4. Bridging theory (TAM, UTAUT, SERVQUAL, etc.) with aviation practice

Always respond in the requested language (Thai or English)."""

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        message = input_data.get("message", "")
        language = input_data.get("language", "th")

        prompt = f"""Generate 5 research topics for aviation management research.
Language: {language}
Request: {message}

For each topic provide:
1. Full research title
2. Research domain
3. Suggested theory/framework
4. Key variables (IV, DV, Mediators)
5. Target journal
6. Novelty explanation"""

        response = await self.get_llm_response(prompt, self.system_prompt)

        return {
            "response": response,
            "suggestions": [
                "Consider post-COVID recovery context",
                "Focus on digital transformation themes",
                "Include sustainability dimension",
            ],
            "next_steps": [
                "Run literature review for selected topic",
                "Check for existing similar studies",
                "Consult with thesis advisor",
            ],
        }

    async def generate(self, request: TopicGenerationRequest) -> TopicGenerationResponse:
        prompt = f"""Generate aviation research topics for:
Domain: {request.domain}
Research Level: {request.research_level}
Keywords: {', '.join(request.keywords or [])}
Theory: {request.preferred_theory or 'Any appropriate theory'}"""

        response = await self.get_llm_response(prompt, self.system_prompt)

        return TopicGenerationResponse(
            topics=[
                {"title": "AI Adoption in Airline Operations", "theory": "TAM", "domain": request.domain},
                {"title": "Digital Transformation in Airport Services", "theory": "UTAUT2", "domain": request.domain},
                {"title": "Sustainable Aviation Practices and Passenger Satisfaction", "theory": "ECT", "domain": request.domain},
            ],
            gaps=["Post-pandemic recovery studies", "AI ethics in aviation", "Green aviation adoption"],
            recommendations=response,
            domain_context=f"Aviation {request.domain} research context with {request.research_level} level requirements",
        )
