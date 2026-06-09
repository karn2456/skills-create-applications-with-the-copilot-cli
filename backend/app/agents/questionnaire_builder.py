from app.agents.base_agent import BaseAgent
from typing import Any, Dict, Optional


class QuestionnaireBuilderAgent(BaseAgent):
    def __init__(self):
        super().__init__("questionnaire", "Questionnaire Builder Agent")

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        message = input_data.get("message", "")
        language = input_data.get("language", "th")

        system_prompt = """You are an expert Questionnaire Designer for Aviation Research.
Create validated Likert-scale questionnaires (5-point or 7-point scale).
Generate both Thai and English versions with proper construct validity.
Include demographic questions appropriate for aviation research context."""

        response = await self.get_llm_response(
            f"Build questionnaire: {message} (Language: {language})",
            system_prompt
        )

        return {
            "response": response,
            "suggestions": ["Pilot test with 30 respondents", "Check content validity with experts"],
            "next_steps": ["Collect data", "Run reliability analysis"],
        }
