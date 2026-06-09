from app.agents.base_agent import BaseAgent
from typing import Any, Dict, Optional


class PaperWriterAgent(BaseAgent):
    def __init__(self):
        super().__init__("paper-writing", "Paper Writing Agent")

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        message = input_data.get("message", "")
        language = input_data.get("language", "th")

        system_prompt = """You are an expert Academic Writer specialized in Aviation Management research.
You can write complete thesis chapters (1-5), research papers, conference papers, and Scopus-indexed articles.
Follow APA 7th edition formatting strictly.
For Thai theses, follow Thai academic writing conventions while maintaining academic rigor."""

        response = await self.get_llm_response(
            f"Write academic content: {message} (Language: {language})",
            system_prompt
        )

        return {
            "response": response,
            "suggestions": ["Check APA formatting", "Verify citations are complete"],
            "next_steps": ["Review with supervisor", "Run plagiarism check"],
        }
