from app.agents.base_agent import BaseAgent
from typing import Any, Dict, Optional


class SEMExpertAgent(BaseAgent):
    def __init__(self):
        super().__init__("sem-expert", "SEM/CFA Expert Agent")

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        message = input_data.get("message", "")
        language = input_data.get("language", "th")

        system_prompt = """You are an expert in Structural Equation Modeling (SEM) and Confirmatory Factor Analysis (CFA) for Aviation Research.
Provide detailed guidance on:
- CFA model validation (loadings, CR, AVE, HTMT)
- SEM model fit indices (CFI, TLI, RMSEA, SRMR)
- PLS-SEM with SmartPLS
- AMOS syntax generation
- Mediation and moderation analysis
- Common method bias assessment
Explain concepts clearly in Thai or English."""

        response = await self.get_llm_response(
            f"SEM/CFA analysis: {message} (Language: {language})",
            system_prompt
        )

        return {
            "response": response,
            "suggestions": ["Check CR > 0.7", "Verify AVE > 0.5", "HTMT < 0.85"],
            "next_steps": ["Run model modification", "Report fit indices"],
        }
