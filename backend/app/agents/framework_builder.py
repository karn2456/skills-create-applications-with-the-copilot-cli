from app.agents.base_agent import BaseAgent
from typing import Any, Dict, Optional


class FrameworkBuilderAgent(BaseAgent):
    def __init__(self):
        super().__init__("framework-builder", "Conceptual Framework Agent")

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        message = input_data.get("message", "")
        language = input_data.get("language", "th")

        system_prompt = """You are an expert Conceptual Framework Designer for Aviation Research.
You specialize in building research frameworks using TAM, UTAUT, SERVQUAL, ECT, RBV, TOE, and other theories.
Design clear, publishable conceptual frameworks with hypotheses, mediators, and moderators."""

        response = await self.get_llm_response(
            f"Build conceptual framework: {message} (Language: {language})",
            system_prompt
        )

        return {
            "response": response,
            "suggestions": ["Validate with theory", "Check for mediating variables"],
            "next_steps": ["Generate hypotheses", "Create questionnaire"],
        }
