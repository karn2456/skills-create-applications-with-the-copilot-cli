"""
Phase 1-B — Literature Synthesis Agent
Reads the paper catalog from LiteratureSearchAgent, synthesizes themes,
maps theoretical frameworks, and identifies contradictions / research gaps.
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent
from ..core.session import ResearchPhase


class SynthesisAgent(BaseResearchAgent):

    NAME = "synthesis"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.DISCOVERY, session, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are an expert Aviation Literature Synthesis Agent.

Your role: transform a raw paper catalog into a structured knowledge map that reveals:
- What is known (consensus findings)
- What is contested (conflicting evidence)
- What is missing (research gaps)

Synthesis frameworks you apply:
1. **Thematic Synthesis** (Thomas & Harden, 2008) — for qualitative integration
2. **Meta-analysis approach** — for quantitative studies (effect size estimation)
3. **Concept matrix** (Webster & Watson, 2002) — rows = papers, cols = concepts
4. **TCCM framework** (Theory, Context, Characteristics, Methodology) for IS-style reviews
5. **Theoretical framework mapping** — which theories are most used, underused, absent

Aviation-specific synthesis patterns:
- Safety models: Swiss Cheese, HFACS, STAMP/STPA, Bow-tie
- Human factors models: SHELL, SHEL, GEMS, SEIPS
- Organizational: High Reliability Organizations (HRO), Safety Management System (SMS)
- Cultural frameworks: Hofstede in aviation context, Power Distance and CRM
- Statistical: meta-regression for publication bias, funnel plot interpretation

Critical synthesis skills:
- Identify where studies use the same construct with different operationalizations
- Flag methodological limitations that weaken a body of evidence
- Spot publication bias indicators (only positive results published)
- Connect findings across aviation sub-domains (MRO ↔ flight operations ↔ ATC)

Output: Structured synthesis document with:
- Thematic map (visual ASCII representation)
- Theoretical framework recommendation with justification
- Evidence table (finding → strength of evidence → papers)
- Contradiction analysis
- Research gap taxonomy (level: conceptual / methodological / empirical / contextual)"""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "build_concept_matrix",
                "description": "Build a concept matrix from a list of papers",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "papers": {"type": "array", "items": {"type": "string"}},
                        "concepts": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["papers", "concepts"],
                },
            },
            {
                "name": "identify_theoretical_framework",
                "description": "Recommend the most appropriate theoretical framework",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "domain": {"type": "string"},
                        "research_question": {"type": "string"},
                        "study_type": {
                            "type": "string",
                            "enum": ["quantitative", "qualitative", "mixed"],
                        },
                    },
                    "required": ["domain", "research_question"],
                },
            },
        ]

    def synthesize(self, literature_catalog: str) -> str:
        return self.run(
            task=f"""Synthesize this aviation literature catalog into a structured knowledge map:

{literature_catalog[:3000]}

Produce:
1. Thematic synthesis map (ASCII tree: Topic → Sub-themes → Key findings)
2. Theoretical framework landscape (what theories dominate, what's missing)
3. Evidence strength table per sub-theme (Strong / Moderate / Weak / Absent)
4. Contradiction register (paired conflicting findings with possible explanations)
5. Research gap taxonomy:
   - Conceptual gaps (theory not yet applied to this domain)
   - Methodological gaps (methodologies missing from the literature)
   - Empirical gaps (populations / contexts not studied)
   - Contextual gaps (Thai aviation, developing-country aviation specifically)
6. "Most promising" research directions (ranked top 5)""",
            artifact_type="synthesis_map",
            artifact_title="Literature Synthesis & Knowledge Map",
        )
