"""
Long-horizon research memory — inspired by Orchestra's Total Recall.
Indexes research sessions, findings, dead ends, and agent outputs.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


@dataclass
class MemoryEntry:
    id: str
    agent: str
    type: str          # "finding" | "dead_end" | "hypothesis" | "result"
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class ResearchMemory:
    """Persistent long-horizon memory store for the aviation research platform."""

    def __init__(self, session_id: str, store_path: str = ".research_memory"):
        self.session_id = session_id
        self.store_path = Path(store_path)
        self.store_path.mkdir(exist_ok=True)
        self._entries: list[MemoryEntry] = []
        self._load()

    def add(self, agent: str, type_: str, content: str, **metadata) -> MemoryEntry:
        entry = MemoryEntry(
            id=f"{agent}_{int(time.time() * 1000)}",
            agent=agent,
            type=type_,
            content=content,
            metadata=metadata,
        )
        self._entries.append(entry)
        self._persist()
        return entry

    def search(self, query: str, agent: str | None = None, limit: int = 10) -> list[MemoryEntry]:
        results = [
            e for e in self._entries
            if query.lower() in e.content.lower()
            and (agent is None or e.agent == agent)
        ]
        return sorted(results, key=lambda e: e.timestamp, reverse=True)[:limit]

    def get_context_summary(self) -> str:
        """Return a compact context summary for injection into agent prompts."""
        if not self._entries:
            return "No prior research context."
        recent = sorted(self._entries, key=lambda e: e.timestamp, reverse=True)[:5]
        lines = ["=== Prior Research Context ==="]
        for e in recent:
            lines.append(f"[{e.agent}] {e.type}: {e.content[:200]}")
        return "\n".join(lines)

    def _persist(self):
        path = self.store_path / f"{self.session_id}.json"
        path.write_text(json.dumps([asdict(e) for e in self._entries], indent=2))

    def _load(self):
        path = self.store_path / f"{self.session_id}.json"
        if path.exists():
            data = json.loads(path.read_text())
            self._entries = [MemoryEntry(**d) for d in data]
