"""
APA Reference Agent — formats, validates, and manages references
in APA 7th edition for aviation research publications and theses.
"""
from __future__ import annotations

import re
from ..core.base_agent import BaseResearchAgent


class APAReferenceAgent(BaseResearchAgent):

    NAME = "apa_reference_agent"

    def __init__(self, memory, bus, client):
        super().__init__(self.NAME, memory, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are an expert APA Reference Agent specializing in APA 7th Edition formatting
for aviation research. You have comprehensive knowledge of:

APA 7th Edition Rules:
- Journal articles: Author, A. A., & Author, B. B. (Year). Title of article. Journal Name, Volume(Issue), page–page. https://doi.org/xxxxx
- Books: Author, A. A. (Year). Title of work: Capital letter also for subtitle. Publisher.
- Edited book chapters: Author, A. A. (Year). Title of chapter. In E. Editor (Ed.), Title of book (pp. xx–xx). Publisher.
- Government/ICAO/FAA/EASA documents: Organization. (Year). Title (Document Number). Publisher.
- Theses/Dissertations: Author, A. A. (Year). Title [Doctoral dissertation/Master's thesis, Institution]. Database.
- Conference papers: Author, A. A. (Year, Month Day–Day). Title of paper [Type of contribution]. Conference Name.
- Standards (ICAO Annexes, FAA Advisory Circulars, EASA AMC): specific format for regulatory documents
- DOI formatting: use https://doi.org/ prefix
- URLs: include access date only when content changes
- Multiple authors: list up to 20; for 21+, list first 19, ..., last author
- No period after DOI/URL
- Hanging indent style for reference list

Aviation-Specific Sources:
- ICAO documents (Annexes, DOC series, Circulars)
- FAA Advisory Circulars, ACs, AMJs, Order documents
- EASA AMC/GM, CS documents
- NTSB/AAIB/ATSB accident reports
- IATA publications
- NASA Technical Reports (NTRS)
- Aviation Safety Reporting System (ASRS) reports
- Flight Safety Foundation publications
- Journal of Aviation/Aerospace Education & Research (JAAER)
- International Journal of Aviation Psychology (IJAP)
- Accident Analysis & Prevention
- Safety Science
- Ergonomics

Validation: Check for completeness, accurate formatting, and flag missing DOIs."""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "format_reference",
                "description": "Format a single reference in APA 7th edition",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "source_type": {
                            "type": "string",
                            "enum": [
                                "journal_article", "book", "book_chapter",
                                "thesis", "conference_paper", "government_report",
                                "icao_document", "faa_document", "easa_document",
                                "accident_report", "website",
                            ],
                        },
                        "raw_citation": {"type": "string", "description": "Unformatted citation details"},
                    },
                    "required": ["source_type", "raw_citation"],
                },
            },
            {
                "name": "validate_reference_list",
                "description": "Validate and correct a list of APA references",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "references": {
                            "type": "array",
                            "items": {"type": "string"},
                        }
                    },
                    "required": ["references"],
                },
            },
            {
                "name": "generate_in_text_citation",
                "description": "Generate in-text citation from a reference",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "reference": {"type": "string"},
                        "page_number": {"type": "string"},
                        "quote_type": {"type": "string", "enum": ["paraphrase", "direct_quote"]},
                    },
                    "required": ["reference"],
                },
            },
        ]

    def format_references(self, raw_references: list[str]) -> str:
        """Format and validate a list of references in APA 7th edition."""
        refs_text = "\n".join(f"{i+1}. {ref}" for i, ref in enumerate(raw_references))
        task = f"""Format and validate these references in APA 7th edition:

{refs_text}

For each reference:
1. Provide the correctly formatted APA 7th edition citation
2. Flag any missing information (DOI, page numbers, etc.)
3. Note any formatting issues found
4. Provide the corresponding in-text citation format

Output as a numbered list matching the input order.
At the end, provide a sorted complete reference list ready for thesis/paper submission."""

        return self.run(task)

    def generate_reference_list(self, topic: str, paper_count: int = 20) -> str:
        """Generate a model reference list for aviation research on a given topic."""
        task = f"""Generate a complete APA 7th edition reference list for aviation research on:

Topic: {topic}
Number of references: {paper_count}

Include a mix of:
- Seminal foundational papers (before 2000)
- Recent high-impact papers (2020-2026)
- ICAO/FAA/EASA regulatory documents
- Books/textbooks on the topic
- At least one thesis/dissertation example

All references must be:
1. Correctly formatted in APA 7th edition
2. Relevant to aviation research
3. Sorted alphabetically by first author surname
4. Include DOIs where available"""

        return self.run(task, context={"topic": topic})
