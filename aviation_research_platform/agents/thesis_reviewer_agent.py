"""
Thesis Reviewer Agent — reviews aviation research theses and dissertations
for academic quality, structural integrity, and aviation domain rigor.
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent
from ..core.session import ResearchPhase


class ThesisReviewerAgent(BaseResearchAgent):

    NAME = "thesis_reviewer"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.PUBLICATION, session, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are an expert Thesis Reviewer Agent for Aviation Research with the
perspective of a senior academic committee member at a graduate aviation program.

Your review expertise covers:
1. Academic Writing Quality
   - Clarity, coherence, and academic register
   - Logical flow between sections
   - Paragraph structure (PEEL: Point, Evidence, Explanation, Link)
   - Avoidance of colloquialism, first-person misuse, hedge language

2. Research Design Quality
   - Research question clarity and feasibility
   - Alignment: RQ → Objectives → Hypotheses → Methodology → Analysis → Conclusions
   - Appropriate methodology for aviation context (quantitative/qualitative/mixed)
   - Sampling strategy validity (aviation-specific: airline, MRO, ATC, GA, military)
   - Ethical considerations (IATA, ICAO research ethics; operational data sensitivity)

3. Literature Review Quality
   - Theoretical framework appropriateness and justification
   - Coverage of seminal and recent literature
   - Critical synthesis (not just description)
   - Identification of research gap (must be explicit and convincing)

4. Methodology Chapter
   - Ontology/epistemology alignment
   - Research paradigm justification
   - Instrument validity and reliability evidence
   - Data collection procedure (aviation access challenges, confidentiality)

5. Results & Analysis
   - Statistical analysis appropriateness
   - Correct interpretation of SEM/regression/ANOVA results
   - Visual presentation (tables, figures per APA 7th)
   - Aviation safety data handling (ICAO Annex 13 protections)

6. Discussion & Conclusion
   - RQ answered directly
   - Theoretical contribution
   - Practical implications for aviation industry (regulatory, operational)
   - Limitations acknowledged appropriately
   - Future research directions

7. Aviation Industry Alignment
   - Regulatory context (ICAO SARPs, EASA regulations, FAA FARs)
   - Industry standards referenced (IATA AHM, MOPS, SMS frameworks)
   - Operational realism of recommendations

Review Output Format:
- Chapter-by-chapter assessment with specific scores
- Strengths and weaknesses per section
- Specific revision recommendations with examples
- Overall recommendation: Pass / Minor Revisions / Major Revisions / Fail"""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "check_alignment",
                "description": "Check alignment between research questions, objectives, and methodology",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "research_questions": {"type": "array", "items": {"type": "string"}},
                        "objectives": {"type": "array", "items": {"type": "string"}},
                        "hypotheses": {"type": "array", "items": {"type": "string"}},
                        "methodology": {"type": "string"},
                    },
                    "required": ["research_questions", "methodology"],
                },
            },
            {
                "name": "review_chapter",
                "description": "Detailed review of a specific thesis chapter",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "chapter": {
                            "type": "string",
                            "enum": [
                                "introduction", "literature_review", "methodology",
                                "results", "discussion", "conclusion",
                            ],
                        },
                        "content": {"type": "string", "description": "Chapter text to review"},
                    },
                    "required": ["chapter", "content"],
                },
            },
            {
                "name": "generate_feedback_report",
                "description": "Generate a structured viva (oral defense) preparation report",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "thesis_summary": {"type": "string"},
                        "weaknesses": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["thesis_summary"],
                },
            },
        ]

    def review(self, thesis_section: str, chapter: str) -> str:
        """Review a thesis section with detailed academic feedback."""
        task = f"""Review the following aviation research thesis {chapter} chapter:

=== CHAPTER: {chapter.upper()} ===
{thesis_section}

Provide:
1. Chapter assessment (score 1-10 with justification)
2. Strengths (specific with quotes)
3. Weaknesses (specific with quotes)
4. Required revisions (numbered list, high priority first)
5. Suggested revision examples (rewrite 2-3 problematic sentences)
6. Aviation domain-specific feedback
7. APA formatting issues (if any)"""

        return self.run(task, context={"chapter": chapter})

    def generate_viva_questions(self, thesis_abstract: str, research_questions: list[str]) -> str:
        """Generate likely viva questions for thesis defense preparation."""
        task = f"""Generate viva (oral defense) preparation questions for:

Abstract: {thesis_abstract}

Research Questions:
{chr(10).join(f'RQ{i+1}: {rq}' for i, rq in enumerate(research_questions))}

Generate:
1. 10 likely examiner questions (with suggested answer strategies)
2. 5 methodology challenge questions (with defense strategies)
3. 5 aviation industry implication questions
4. 3 "what would you do differently" questions
5. Opening statement recommendation (2 minutes)"""

        return self.run(task)
