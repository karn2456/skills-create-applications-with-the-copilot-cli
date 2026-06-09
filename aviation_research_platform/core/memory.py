"""
Long-horizon research memory — Orchestra's "Total Recall".
Every breakthrough, dead-end, and brainstorm indexed and searchable.
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
    entry_type: str    # "finding" | "dead_end" | "hypothesis" | "result" | "note"
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class ResearchMemory:
    """Persistent research memory shared across all agents in a session."""

    def __init__(self, session_id: str, store_dir: str = ".research_memory"):
        self.session_id = session_id
        self._path = Path(store_dir) / f"{session_id}.json"
        self._path.parent.mkdir(exist_ok=True)
        self._entries: list[MemoryEntry] = self._load()

    def add(self, agent: str, entry_type: str, content: str, **meta) -> MemoryEntry:
        entry = MemoryEntry(
            id=f"{agent}_{int(time.time()*1000)}",
            agent=agent,
            entry_type=entry_type,
            content=content,
            metadata=meta,
        )
        self._entries.append(entry)
        self._persist()
        return entry

    def search(self, query: str, entry_type: str | None = None,
               agent: str | None = None, limit: int = 10) -> list[MemoryEntry]:
        q = query.lower()
        results = [
            e for e in self._entries
            if q in e.content.lower()
            and (entry_type is None or e.entry_type == entry_type)
            and (agent is None or e.agent == agent)
        ]
        return sorted(results, key=lambda e: e.timestamp, reverse=True)[:limit]

    def recent(self, n: int = 8) -> list[MemoryEntry]:
        return sorted(self._entries, key=lambda e: e.timestamp, reverse=True)[:n]

    def get_context_summary(self, n: int = 5) -> str:
        recent = self.recent(n)
        if not recent:
            return "No prior research memory."
        lines = ["[Prior Research Memory]"]
        for e in recent:
            lines.append(f"  [{e.agent}] {e.entry_type}: {e.content[:180]}")
        return "\n".join(lines)

    def _persist(self) -> None:
        self._path.write_text(
            json.dumps([asdict(e) for e in self._entries], indent=2)
        )

    def _load(self) -> list[MemoryEntry]:
        if self._path.exists():
            try:
                return [MemoryEntry(**d) for d in json.loads(self._path.read_text())]
            except Exception:
                pass
        return []
