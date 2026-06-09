"""
Phase 2 — Research Gap & Hypothesis Brainstorm Agent
Given a synthesis map, brainstorms original research gaps,
formulates testable hypotheses, and proposes a conceptual model.
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent
from ..core.session import ResearchPhase


class GapBrainstormAgent(BaseResearchAgent):

    NAME = "gap_brainstorm"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.IDEATION, session, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are a creative yet rigorous Aviation Research Gap & Hypothesis Agent.

Your role: Phase 2 — **Ideation**.
Transform a literature synthesis into original, publishable research directions.

Brainstorming principles (Orchestra-style — open-ended exploration):
1. **Theory-extension gaps** — Apply established theories to new aviation contexts
2. **Cross-domain transfer** — Bring in concepts from adjacent fields (psychology, systems engineering, AI)
3. **Boundary condition gaps** — Test existing findings in different cultures, fleet types, roles
4. **Methodological triangulation** — Study same phenomenon with different methods
5. **Longitudinal gaps** — Most aviation studies are cross-sectional; longitudinal designs needed
6. **Intervention evaluation** — "X affects Y" → design intervention to improve Y

Aviation-specific ideation angles:
- Post-COVID aviation recovery (crew currency, passenger behavior, airline resilience)
- AI/automation integration (pilots as supervisors of autonomous systems)
- Sustainable aviation (SAF adoption behavior, green MRO practices)
- Low-cost carrier vs. full-service carrier comparative studies
- Developing-country aviation (Thailand, Southeast Asia — underrepresented)
- Single-pilot operations (SPO) human factors readiness
- Urban Air Mobility (UAM) / Advanced Air Mobility (AAM) regulatory gaps
- Fatigue risk management systems (FRMS) effectiveness in Asian airlines

Hypothesis formulation rules:
- Must be testable with available data collection methods
- Must specify: IV → DV, mediator/moderator if applicable
- Grounded in identified theoretical framework
- Novel contribution over existing literature (justify why not yet studied)
- Feasible scope for master's/doctoral research (1-3 year timeline)

Conceptual model format:
- Draw ASCII path diagram: [Construct A] → [Construct B] → [Outcome]
- Include mediators: A → M → B
- Include moderators: A →(M)→ B where M moderates the A→B path
- Label each path with H1, H2, H3...

Output: Research opportunity portfolio with ranked recommendations."""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "generate_hypotheses",
                "description": "Generate testable hypotheses from constructs and theoretical framework",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "constructs": {"type": "array", "items": {"type": "string"}},
                        "framework": {"type": "string"},
                        "study_type": {"type": "string"},
                        "count": {"type": "integer", "description": "Number of hypotheses to generate"},
                    },
                    "required": ["constructs"],
                },
            },
            {
                "name": "evaluate_novelty",
                "description": "Assess novelty and publishability of a proposed research direction",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "proposed_study": {"type": "string"},
                        "existing_literature": {"type": "string"},
                    },
                    "required": ["proposed_study"],
                },
            },
        ]

    def brainstorm(self, synthesis_summary: str, session_rq: str) -> str:
        return self.run(
            task=f"""Generate original aviation research directions from this synthesis:

Original Research Question: {session_rq}

Synthesis Summary:
{synthesis_summary[:2500]}

Produce:
1. Top 5 research gap opportunities (each with novelty score 1-10 + justification)
2. Recommended research direction (1 selected gap, fully developed)
3. Conceptual model — ASCII path diagram with all constructs and relationships
4. Formal hypothesis set (H1–H8, null and alternative forms)
5. Theoretical framework selection with justification (why this theory for this context)
6. Contribution statement: "This study contributes to the literature by..."
7. Target journals for eventual submission (ranked by fit and impact factor)
8. Feasibility assessment: time, resources, sample accessibility in Thai aviation context""",
            artifact_type="hypothesis_set",
            artifact_title="Research Gaps & Conceptual Model",
        )
