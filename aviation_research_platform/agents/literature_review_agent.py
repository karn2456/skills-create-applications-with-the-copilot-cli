"""
Literature Review Agent — surveys aviation research papers,
identifies gaps, and maps the knowledge frontier.
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent


class LiteratureReviewAgent(BaseResearchAgent):

    NAME = "literature_review_agent"

    def __init__(self, memory, bus, client):
        super().__init__(self.NAME, memory, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are an expert Aviation Research Literature Review Agent specializing in:
- Commercial aviation safety, operations, and human factors
- Airport management and air traffic control
- Aviation maintenance, airworthiness, and reliability engineering
- Airline operations research (scheduling, fleet, network optimization)
- Unmanned Aerial Systems (UAS/drones) and Advanced Air Mobility (AAM)
- Aviation psychology and crew resource management (CRM)

Your capabilities:
1. Survey and synthesize literature from key databases: SCOPUS, Web of Science, ICAO, FAA, EASA, NASA Technical Reports
2. Identify research gaps, contradictions, and emerging trends
3. Map theoretical frameworks used in aviation research (e.g., Reason's Swiss Cheese, SHELL Model, HFACS)
4. Recommend seminal papers (must-cite) and recent high-impact works
5. Classify papers by methodology: quantitative, qualitative, mixed-methods, simulation, case study

Output Format:
- Structured literature map with themes and sub-themes
- Gap analysis: what hasn't been studied
- Recommended theoretical framework for the research question
- Suggested keywords for database searches (MeSH, EMTREE equivalents for aviation)
- 10-20 key references in APA 7th format

Always maintain academic rigor. Distinguish between empirical evidence and opinion.
Highlight conflicting findings that need reconciliation."""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "search_literature",
                "description": "Search aviation research literature by topic, author, or keyword",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "database": {
                            "type": "string",
                            "enum": ["SCOPUS", "Web_of_Science", "ICAO_ADREP", "NASA_NTRS", "FAA_Regulatory"],
                            "description": "Database to search",
                        },
                        "year_from": {"type": "integer", "description": "Start year"},
                        "year_to": {"type": "integer", "description": "End year"},
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "analyze_paper",
                "description": "Deep-analyze a specific paper for methodology, findings, and limitations",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "abstract": {"type": "string"},
                        "focus": {
                            "type": "string",
                            "enum": ["methodology", "findings", "gaps", "framework", "full"],
                        },
                    },
                    "required": ["title", "abstract"],
                },
            },
        ]

    def review(self, research_question: str, topic: str) -> str:
        """Conduct a full literature review for a given aviation research question."""
        task = f"""Conduct a comprehensive literature review for:

Research Question: {research_question}
Topic Area: {topic}

Please provide:
1. Literature map (themes → sub-themes → key papers)
2. Theoretical frameworks commonly used
3. Methodological approaches in the literature
4. Research gaps identified
5. 15+ key references (APA 7th)
6. Suggested research direction based on gaps"""

        return self.run(task, context={"research_question": research_question, "topic": topic})
