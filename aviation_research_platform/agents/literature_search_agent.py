"""
Phase 1-A — Literature Search Agent
Finds, retrieves, and catalogues papers relevant to the research question.
Covers: SCOPUS, Web of Science, ICAO, NASA NTRS, FAA, EASA, arXiv (aviation AI).
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent
from ..core.session import ResearchPhase


class LiteratureSearchAgent(BaseResearchAgent):

    NAME = "literature_search"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.DISCOVERY, session, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are an expert Aviation Literature Search Agent.

Your role is Phase 1 of the research lifecycle: **Discovery**.
You simulate expert-level literature database searching across:

Databases you cover:
- SCOPUS / Web of Science (peer-reviewed journals)
- ICAO Document Store (Annexes, DOCs, Circulars)
- NASA Technical Reports Server (NTRS)
- FAA Technical Center (ACTLIBRARY)
- EASA Research & Development (Safety Promotion)
- arXiv cs.AI / q-bio for aviation AI applications
- ProQuest Dissertations & Theses (aviation programs)
- NTSB / AAIB / ATSB accident investigation reports
- Flight Safety Foundation (FSF) publications

Aviation-specific journals you prioritize:
1. Accident Analysis & Prevention (Elsevier)
2. Safety Science (Elsevier)
3. International Journal of Aviation Psychology (Taylor & Francis)
4. Journal of Aviation/Aerospace Education & Research (JAAER)
5. Ergonomics (Taylor & Francis)
6. Human Factors (SAGE)
7. Transportation Research Part F
8. Journal of Air Transport Management

Search strategy principles:
- Boolean operators: AND, OR, NOT with field codes (TITLE-ABS-KEY)
- MeSH-equivalent thesaurus for aviation: use ICAO/IATA standardized terminology
- Snowballing: forward & backward citation chaining
- Grey literature: regulatory docs, industry reports, conference proceedings (AIAA, SAE)
- Language: English-primary; flag Thai, Chinese, Japanese aviation studies when relevant

Output per search:
- Search string used (reproducible)
- Number of results before/after screening
- PRISMA-compatible inclusion/exclusion criteria
- Categorized paper list (by sub-theme)
- Top 5 "must-read" papers with abstract summaries
- Identified databases with most coverage"""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "database_search",
                "description": "Execute a structured search on an aviation research database",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "database": {"type": "string"},
                        "search_string": {"type": "string"},
                        "filters": {
                            "type": "object",
                            "properties": {
                                "year_range": {"type": "string"},
                                "document_type": {"type": "string"},
                                "language": {"type": "string"},
                            },
                        },
                    },
                    "required": ["database", "search_string"],
                },
            },
            {
                "name": "build_search_string",
                "description": "Build an optimized Boolean search string from research keywords",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "keywords": {"type": "array", "items": {"type": "string"}},
                        "database_syntax": {"type": "string", "enum": ["SCOPUS", "WoS", "PubMed", "generic"]},
                    },
                    "required": ["keywords"],
                },
            },
        ]

    def search(self, research_question: str, keywords: list[str] | None = None) -> str:
        kw_str = ", ".join(keywords) if keywords else "derived from research question"
        return self.run(
            task=f"""Execute a comprehensive literature search for:

Research Question: {research_question}
Initial Keywords: {kw_str}

Deliver:
1. Refined search strategy (3 Boolean strings for SCOPUS, WoS, grey literature)
2. PRISMA flow diagram (text form): records identified → screened → included
3. Final included paper list organized by theme (min 25 papers)
4. Top 5 must-read papers with structured abstracts (Purpose/Methods/Findings/Implications)
5. Database coverage map: which DB contributed most
6. Recommended snowballing targets (high-citation papers to trace)""",
            artifact_type="literature_catalog",
            artifact_title=f"Literature Search: {research_question[:60]}",
        )
