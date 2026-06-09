from app.agents.base_agent import BaseAgent
from typing import Any, Dict, Optional


class DataAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("data-analysis", "Data Analysis Agent")

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        message = input_data.get("message", "")
        language = input_data.get("language", "th")

        system_prompt = """You are an expert Statistical Analysis consultant for Aviation Research.
You provide step-by-step guidance for SEM, CFA, PLS-SEM, regression, mediation, and moderation analysis.
Generate APA-style tables and interpret results for thesis/dissertation writing.
Support Jamovi, SPSS, R, STATA, SmartPLS, and AMOS software."""

        response = await self.get_llm_response(
            f"Analyze data: {message} (Language: {language})",
            system_prompt
        )

        return {
            "response": response,
            "suggestions": ["Check sample size adequacy", "Verify normality assumptions"],
            "next_steps": ["Interpret results", "Write Chapter 4"],
        }
