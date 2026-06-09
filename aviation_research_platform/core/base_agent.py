"""
Base agent — foundation for all Aviation Research OS agents.
Each agent owns a specialized system prompt, tools, and shares
the research session + message bus.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import anthropic

from .session import ResearchSession, ResearchPhase
from .message_bus import AgentMessage, MessageBus


class BaseResearchAgent(ABC):

    MODEL = "claude-opus-4-8"

    def __init__(
        self,
        name: str,
        phase: ResearchPhase,
        session: ResearchSession,
        bus: MessageBus,
        client: anthropic.Anthropic,
    ):
        self.name = name
        self.phase = phase
        self.session = session
        self.bus = bus
        self.client = client

    @property
    @abstractmethod
    def system_prompt(self) -> str: ...

    def tools(self) -> list[dict]:
        return []

    def run(self, task: str, artifact_type: str = "result",
            artifact_title: str = "", context: dict[str, Any] | None = None) -> str:

        ctx = self.session.context_summary()
        user_content = f"=== Research Context ===\n{ctx}\n\n=== Task ===\n{task}"
        if context:
            user_content += f"\n\nAdditional context: {json_safe(context)}"

        result = self._call_llm([{"role": "user", "content": user_content}])

        self.session.add_artifact(
            phase=self.phase,
            agent=self.name,
            artifact_type=artifact_type,
            title=artifact_title or task[:80],
            content=result,
        )
        self.bus.publish(AgentMessage(
            sender=self.name,
            receiver="orchestrator",
            message_type="result",
            payload={"task": task, "result": result, "artifact_type": artifact_type},
        ))
        return result

    def _call_llm(self, messages: list[dict], max_tokens: int = 4096) -> str:
        agent_tools = self.tools()
        kwargs: dict[str, Any] = {
            "model": self.MODEL,
            "max_tokens": max_tokens,
            "system": self.system_prompt,
            "messages": messages,
        }
        if agent_tools:
            kwargs["tools"] = agent_tools

        response = self.client.messages.create(**kwargs)
        return "\n".join(
            block.text for block in response.content if hasattr(block, "text")
        )


def json_safe(obj: Any) -> str:
    import json
    try:
        return json.dumps(obj, ensure_ascii=False, default=str)
    except Exception:
        return str(obj)
