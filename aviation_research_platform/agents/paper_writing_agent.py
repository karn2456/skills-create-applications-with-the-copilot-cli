"""
Phase 6 — Paper Writing Agent
Drafts full academic paper sections: Abstract, Introduction, Literature Review,
Methodology, Results, Discussion, Conclusion — in target journal style.
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent
from ..core.session import ResearchPhase

AVIATION_JOURNALS = {
    "AAP": {
        "name": "Accident Analysis & Prevention",
        "publisher": "Elsevier",
        "if": 6.376,
        "style": "structured abstract (Highlights), 8000 words max",
    },
    "SS": {
        "name": "Safety Science",
        "publisher": "Elsevier",
        "if": 5.762,
        "style": "unstructured abstract, 10000 words",
    },
    "IJAP": {
        "name": "International Journal of Aviation Psychology",
        "publisher": "Taylor & Francis",
        "if": 2.1,
        "style": "APA style, 8000 words",
    },
    "HF": {
        "name": "Human Factors",
        "publisher": "SAGE",
        "if": 3.956,
        "style": "structured abstract, 7500 words",
    },
    "JATM": {
        "name": "Journal of Air Transport Management",
        "publisher": "Elsevier",
        "if": 4.2,
        "style": "highlights + keywords, 8000 words",
    },
    "JAAER": {
        "name": "Journal of Aviation/Aerospace Education & Research",
        "publisher": "Embry-Riddle",
        "if": 0.8,
        "style": "APA, open-access friendly for Thai academia",
    },
}


class PaperWritingAgent(BaseResearchAgent):

    NAME = "paper_writing"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.WRITING, session, bus, client)

    @property
    def system_prompt(self) -> str:
        journals_info = "\n".join(
            f"  - {code}: {info['name']} (IF {info['if']}) — {info['style']}"
            for code, info in AVIATION_JOURNALS.items()
        )
        return f"""You are an expert Aviation Research Paper Writing Agent.

Your role: Phase 6 — **Writing**.
Draft publication-quality academic paper sections for aviation research journals.

Target journals available:
{journals_info}

Writing principles (by section):

**Abstract** (250 words max):
- Background (1-2 sentences): why this matters
- Objective (1 sentence): what this study does
- Methods (2-3 sentences): design, sample, instrument, analysis
- Results (2-3 sentences): key findings with numbers
- Conclusions (1-2 sentences): implications + contribution

**Introduction** (800-1200 words):
- Hook: aviation safety statistic or recent incident relevance
- Problem statement: gap in practice or knowledge
- Literature justification: what is known, what is missing
- Study purpose statement (explicit)
- Research questions (numbered)
- Significance: theoretical + practical contributions
- Paper structure outline (last paragraph)

**Literature Review** (2000-3500 words):
- Theory section: name and explain the theoretical framework
- Sub-sections per construct (definition, measurement history, aviation evidence)
- Hypothesis development: each H derived from theory + evidence
- Conceptual model presentation

**Methodology** (1500-2500 words):
- Research design (paradigm, approach, strategy)
- Population and sample (N, characteristics, access)
- Instrumentation (each scale: name, original source, items, α)
- Data collection procedure
- Data analysis approach

**Results** (1500-2000 words):
- Respondent profile (table)
- Measurement model (tables: loadings, AVE, CR, HTMT)
- Structural model (path diagram description + table)
- Hypothesis outcomes (summary table)

**Discussion** (1500-2500 words):
- Restate key findings (don't repeat numbers)
- Theoretical implications (what this adds to theory)
- Practical implications for aviation industry (specific, actionable)
- Comparison to prior studies
- Limitations and future research

**Conclusion** (400-600 words):
- Summary of study purpose and findings
- Theoretical contribution
- Practical recommendations (policy, training, regulation)
- Future research agenda

Academic writing standards:
- Avoid first person "I/we" in passive-heavy journals; use active where journal allows
- Hedging language: "suggests", "indicates", "may", "appears to"
- Citation density: 1-3 citations per key claim
- Avoid overclaiming: "this study proves" → "this study provides evidence"
- Spell out acronyms on first use
- Use present tense for established facts, past tense for study-specific findings"""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "draft_section",
                "description": "Draft a specific paper section",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "section": {
                            "type": "string",
                            "enum": ["abstract", "introduction", "literature_review",
                                     "methodology", "results", "discussion", "conclusion"],
                        },
                        "target_journal": {
                            "type": "string",
                            "enum": list(AVIATION_JOURNALS.keys()),
                        },
                        "word_count_target": {"type": "integer"},
                    },
                    "required": ["section"],
                },
            },
            {
                "name": "improve_writing",
                "description": "Improve academic writing quality of a text passage",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "improvement_focus": {
                            "type": "string",
                            "enum": ["clarity", "academic_tone", "argument_flow",
                                     "citation_integration", "conciseness"],
                        },
                    },
                    "required": ["text"],
                },
            },
        ]

    def draft_section(self, section: str, content_brief: str,
                      target_journal: str = "AAP") -> str:
        journal = AVIATION_JOURNALS.get(target_journal, AVIATION_JOURNALS["AAP"])
        return self.run(
            task=f"""Draft the {section.upper()} section for:

Target Journal: {journal['name']} ({journal['style']})
Research context from session memory (see above)

Section-specific content brief:
{content_brief}

Write a complete, publication-ready {section} section.
Follow journal guidelines. Use APA 7th in-text citations.
Aim for appropriate word count for this section and journal.""",
            artifact_type=f"draft_{section}",
            artifact_title=f"Draft: {section.title()} — {journal['name']}",
        )

    def draft_full_paper(self, analysis_summary: str, target_journal: str = "AAP") -> str:
        journal = AVIATION_JOURNALS.get(target_journal, AVIATION_JOURNALS["AAP"])
        return self.run(
            task=f"""Draft a complete aviation research paper outline + key sections for:

Target Journal: {journal['name']}
Journal Guidelines: {journal['style']}

Analysis Summary:
{analysis_summary[:2000]}

Produce:
1. Title (3 options, ranked)
2. Abstract (complete, {journal['style'].split(',')[0] if ',' in journal['style'] else '250 words'})
3. Introduction (full draft, ~1000 words)
4. Hypothesis summary table (H# | IV | DV | Direction | Supported?)
5. Discussion key paragraphs (theoretical + practical implications)
6. Conclusion (complete)
7. Suggested keywords (6-8, journal style)
8. Cover letter draft for submission""",
            artifact_type="full_paper_draft",
            artifact_title=f"Full Paper Draft — {journal['name']}",
        )
