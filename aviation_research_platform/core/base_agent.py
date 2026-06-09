"""
Base agent class — all Aviation Research agents inherit from this.
Mirrors the agent pattern in both Orchestra (Cognitive Layer) and GitLab Duo (sub-agents).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import anthropic

from .memory import ResearchMemory
from .message_bus import AgentMessage, MessageBus


class BaseResearchAgent(ABC):
    """
    Foundation for all Aviation Research Platform agents.

    Each agent has:
    - A specialized system prompt (domain expertise)
    - Access to shared research memory (long-horizon context)
    - Message bus for inter-agent communication
    - Tool definitions for structured output
    """

    MODEL = "claude-opus-4-8"  # Use most capable model for research agents

    def __init__(
        self,
        name: str,
        memory: ResearchMemory,
        bus: MessageBus,
        client: anthropic.Anthropic,
    ):
        self.name = name
        self.memory = memory
        self.bus = bus
        self.client = client

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Domain-specific system prompt for this agent."""

    @abstractmethod
    def tools(self) -> list[dict]:
        """Anthropic tool definitions this agent can use."""

    def run(self, task: str, context: dict[str, Any] | None = None) -> str:
        """Execute a research task and return the result."""
        prior_context = self.memory.get_context_summary()

        messages = [
            {
                "role": "user",
                "content": (
                    f"{prior_context}\n\n"
                    f"=== Current Task ===\n{task}"
                    + (f"\n\nContext: {context}" if context else "")
                ),
            }
        ]

        result = self._call_llm(messages)
        self.memory.add(self.name, "result", result, task=task)
        self.bus.publish(AgentMessage(
            sender=self.name,
            receiver="orchestrator",
            message_type="result",
            payload={"task": task, "result": result},
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

        # Collect all text content blocks
        text_blocks = [
            block.text
            for block in response.content
            if hasattr(block, "text")
        ]
        return "\n".join(text_blocks)
