from app.agents.base_agent import BaseAgent
from typing import Any, Dict, Optional


class ThesisSupervisorAgent(BaseAgent):
    def __init__(self):
        super().__init__("thesis-supervisor", "Thesis Supervisor Agent")

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        message = input_data.get("message", "")
        language = input_data.get("language", "th")

        system_prompt = """You are an expert Thesis Supervisor (อาจารย์ที่ปรึกษาดิจิทัล) for Aviation Management research.
Review thesis chapters critically and provide constructive feedback like a senior academic advisor.
Check for:
- Alignment between objectives, hypotheses, and framework
- Literature review adequacy
- Methodology appropriateness
- Results interpretation accuracy
- APA formatting compliance
Provide specific, actionable improvement suggestions."""

        response = await self.get_llm_response(
            f"Review thesis content: {message} (Language: {language})",
            system_prompt
        )

        return {
            "response": response,
            "suggestions": ["Address all reviewer comments", "Update literature review"],
            "next_steps": ["Revise chapters", "Schedule defense"],
        }
