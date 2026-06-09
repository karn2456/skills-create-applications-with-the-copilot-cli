"""
Research Session — tracks the full lifecycle state of a research project.
Mirrors Orchestra's concept of a "Research Quest" — long-horizon, stateful,
multi-phase research journey.

Phases follow the Orchestra workflow:
  DISCOVERY → IDEATION → DESIGN → EXECUTION → ANALYSIS → WRITING → PUBLICATION
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any


class ResearchPhase(str, Enum):
    DISCOVERY   = "discovery"    # 1. Literature search & survey
    IDEATION    = "ideation"     # 2. Synthesis + gap brainstorm
    DESIGN      = "design"       # 3. Experiment / questionnaire design
    EXECUTION   = "execution"    # 4. Run code / collect data
    ANALYSIS    = "analysis"     # 5. Statistical analysis
    WRITING     = "writing"      # 6. Draft paper sections
    PUBLICATION = "publication"  # 7. Format, submit, respond to reviewers


PHASE_ORDER = [
    ResearchPhase.DISCOVERY,
    ResearchPhase.IDEATION,
    ResearchPhase.DESIGN,
    ResearchPhase.EXECUTION,
    ResearchPhase.ANALYSIS,
    ResearchPhase.WRITING,
    ResearchPhase.PUBLICATION,
]


@dataclass
class PhaseArtifact:
    """A concrete output produced by an agent in a phase."""
    phase: str
    agent: str
    artifact_type: str   # "literature_map" | "hypothesis" | "instrument" | "code" | "draft" | ...
    title: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


@dataclass
class ResearchSession:
    """
    The complete state of a research project session.
    Persisted to disk so researchers can resume weeks later (Orchestra's Total Recall).
    """
    session_id: str
    research_question: str
    domain: str
    current_phase: ResearchPhase = ResearchPhase.DISCOVERY
    artifacts: list[PhaseArtifact] = field(default_factory=list)
    dead_ends: list[dict] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    research_gaps: list[str] = field(default_factory=list)
    key_papers: list[str] = field(default_factory=list)
    notes: list[dict] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    # ── Persistence ──────────────────────────────────────────────────────────

    def save(self, store_dir: str = ".research_sessions") -> Path:
        path = Path(store_dir)
        path.mkdir(exist_ok=True)
        file = path / f"{self.session_id}.json"
        data = asdict(self)
        file.write_text(json.dumps(data, indent=2, default=str))
        return file

    @classmethod
    def load(cls, session_id: str, store_dir: str = ".research_sessions") -> "ResearchSession":
        file = Path(store_dir) / f"{session_id}.json"
        data = json.loads(file.read_text())
        data["current_phase"] = ResearchPhase(data["current_phase"])
        data["artifacts"] = [PhaseArtifact(**a) for a in data["artifacts"]]
        return cls(**data)

    @classmethod
    def new(cls, research_question: str, domain: str) -> "ResearchSession":
        return cls(
            session_id=str(uuid.uuid4())[:8],
            research_question=research_question,
            domain=domain,
        )

    # ── State mutations ───────────────────────────────────────────────────────

    def add_artifact(self, phase: ResearchPhase, agent: str,
                     artifact_type: str, title: str, content: str, **meta) -> PhaseArtifact:
        artifact = PhaseArtifact(
            phase=phase.value, agent=agent, artifact_type=artifact_type,
            title=title, content=content, metadata=meta,
        )
        self.artifacts.append(artifact)
        self.updated_at = time.time()
        return artifact

    def add_dead_end(self, description: str, agent: str) -> None:
        self.dead_ends.append({"description": description, "agent": agent, "ts": time.time()})

    def advance_phase(self) -> ResearchPhase:
        idx = PHASE_ORDER.index(self.current_phase)
        if idx < len(PHASE_ORDER) - 1:
            self.current_phase = PHASE_ORDER[idx + 1]
        self.updated_at = time.time()
        return self.current_phase

    def get_artifacts_for_phase(self, phase: ResearchPhase) -> list[PhaseArtifact]:
        return [a for a in self.artifacts if a.phase == phase.value]

    def get_latest_artifact(self, artifact_type: str) -> PhaseArtifact | None:
        matches = [a for a in self.artifacts if a.artifact_type == artifact_type]
        return max(matches, key=lambda a: a.created_at) if matches else None

    def context_summary(self, max_artifacts: int = 4) -> str:
        """Compact summary injected into every agent prompt for long-horizon context."""
        lines = [
            f"Session: {self.session_id}",
            f"RQ: {self.research_question}",
            f"Domain: {self.domain}",
            f"Phase: {self.current_phase.value}",
        ]
        if self.hypotheses:
            lines.append(f"Hypotheses: {'; '.join(self.hypotheses[:3])}")
        if self.research_gaps:
            lines.append(f"Gaps found: {'; '.join(self.research_gaps[:3])}")
        if self.dead_ends:
            lines.append(f"Dead ends: {len(self.dead_ends)} recorded")
        recent = sorted(self.artifacts, key=lambda a: a.created_at, reverse=True)[:max_artifacts]
        for a in recent:
            lines.append(f"[{a.agent}] {a.artifact_type}: {a.title}")
        return "\n".join(lines)

    def progress_bar(self) -> str:
        idx = PHASE_ORDER.index(self.current_phase)
        parts = []
        for i, phase in enumerate(PHASE_ORDER):
            if i < idx:
                parts.append(f"✓ {phase.value}")
            elif i == idx:
                parts.append(f"▶ {phase.value}")
            else:
                parts.append(f"  {phase.value}")
        return " → ".join(parts)
