from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from app.config import settings


class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.llm_provider = "anthropic"

    @abstractmethod
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        pass

    async def get_llm_response(self, prompt: str, system_prompt: str = "") -> str:
        if settings.ANTHROPIC_API_KEY:
            return await self._call_anthropic(prompt, system_prompt)
        elif settings.OPENAI_API_KEY:
            return await self._call_openai(prompt, system_prompt)
        else:
            return self._mock_response(prompt)

    async def _call_anthropic(self, prompt: str, system_prompt: str) -> str:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            message = client.messages.create(
                model="claude-opus-4-8",
                max_tokens=4096,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception as e:
            return f"Error calling Anthropic API: {str(e)}"

    async def _call_openai(self, prompt: str, system_prompt: str) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=4096,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"

    def _mock_response(self, prompt: str) -> str:
        return f"[DEMO MODE] Agent {self.name} response for: {prompt[:100]}..."
