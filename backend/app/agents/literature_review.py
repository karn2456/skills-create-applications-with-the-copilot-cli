from app.agents.base_agent import BaseAgent
from typing import Any, Dict, Optional


class LiteratureReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("literature-review", "Literature Review Agent")

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        message = input_data.get("message", "")
        language = input_data.get("language", "th")

        system_prompt = """You are an expert Literature Review specialist for Aviation Management research.
You help researchers find, synthesize, and analyze academic literature.
Create comprehensive literature matrices, identify themes, and spot research gaps.
Format outputs in APA 7th edition style."""

        response = await self.get_llm_response(
            f"Perform literature review task: {message} (Language: {language})",
            system_prompt
        )

        return {
            "response": response,
            "suggestions": ["Search Scopus database", "Check WoS for additional papers"],
            "next_steps": ["Build citation map", "Identify research gaps"],
        }
