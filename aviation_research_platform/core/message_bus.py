"""
Inter-agent message bus — allows agents to pass results and requests.
Mirrors the tool-calling communication pattern in GitLab Duo / Orchestra.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Any, Callable


@dataclass
class AgentMessage:
    sender: str
    receiver: str          # agent name or "orchestrator" or "broadcast"
    message_type: str      # "result" | "request" | "error" | "status"
    payload: dict[str, Any]
    timestamp: float = field(default_factory=time.time)


class MessageBus:
    """Simple synchronous message bus for agent-to-agent communication."""

    def __init__(self):
        self._queues: dict[str, list[AgentMessage]] = defaultdict(list)
        self._handlers: dict[str, list[Callable]] = defaultdict(list)

    def publish(self, message: AgentMessage) -> None:
        self._queues[message.receiver].append(message)
        for handler in self._handlers.get(message.receiver, []):
            handler(message)

    def subscribe(self, receiver: str, handler: Callable) -> None:
        self._handlers[receiver].append(handler)

    def consume(self, receiver: str) -> list[AgentMessage]:
        messages = self._queues.pop(receiver, [])
        return messages

    def broadcast(self, sender: str, message_type: str, payload: dict) -> None:
        msg = AgentMessage(
            sender=sender,
            receiver="broadcast",
            message_type=message_type,
            payload=payload,
        )
        self._queues["broadcast"].append(msg)
