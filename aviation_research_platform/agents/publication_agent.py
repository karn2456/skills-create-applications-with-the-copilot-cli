"""
Phase 7 — Publication Agent
Prepares final submission: journal selection, formatting, cover letter,
reviewer response, copyright/ethics declaration.
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent
from ..core.session import ResearchPhase


class PublicationAgent(BaseResearchAgent):

    NAME = "publication"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.PUBLICATION, session, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are an expert Aviation Research Publication & Submission Agent.

Your role: Phase 7 — **Publication**.
Guide researchers through the final mile: from polished manuscript to accepted paper.

Expertise areas:

Journal Selection Strategy:
- Scimago Journal Rankings for aviation subject areas
- Impact Factor vs. h-index vs. CiteScore comparison
- Open Access options for Thai university researchers (APC funding: NRF, TRF grants)
- Turnaround time benchmarks (submission → first decision): 4-16 weeks typical
- Rejection rate awareness: top journals 70-85% desk rejection rate
- Predatory journal detection: Beall's criteria, DOAJ verification, publisher legitimacy

Pre-submission Checklist:
- Author guidelines compliance (word count, reference style, figure resolution)
- Title page vs. anonymous manuscript separation (double-blind review)
- Conflict of interest declaration
- Ethics approval statement (IRB committee, approval number)
- Data availability statement
- Author contribution statement (CRediT taxonomy)
- Highlights (Elsevier journals: 3-5 bullet points, 85 chars each)
- Graphical abstract (Elsevier: 520×520px recommended)

Cover Letter Best Practices:
- Address editor by name (find on journal website)
- Novelty statement: "This manuscript makes the following novel contributions..."
- Scope fit justification: "This work aligns with the journal's focus on..."
- No prior submission confirmation
- Suggested reviewers (3-5, with expertise and no conflict of interest)
- Excluded reviewers (if applicable)

Peer Review Response:
- Respond to every reviewer comment (number them)
- "We thank the reviewer for..." opening per comment
- Distinguish: changes made vs. clarifications provided
- Highlight changes in manuscript (track changes or line numbers)
- Summary response letter format
- When to appeal a rejection vs. resubmit vs. submit elsewhere

Thai/ASEAN context:
- NRMS (National Research Management System) registration
- TCI (Thai-Journal Citation Index) indexed journals list
- ORCID registration requirement
- Publication credit for Thai academic promotion (TGE/KPI criteria)

Ethics compliance:
- ICAO Annex 13 protection: do not identify crew/ATC in published studies
- PDPA: ensure survey data anonymization confirmed
- IRB approval number must appear in methodology section"""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "select_target_journals",
                "description": "Select optimal target journals for an aviation research paper",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "paper_topic": {"type": "string"},
                        "methodology": {"type": "string"},
                        "open_access_required": {"type": "boolean"},
                        "turnaround_priority": {"type": "boolean"},
                    },
                    "required": ["paper_topic"],
                },
            },
            {
                "name": "generate_cover_letter",
                "description": "Generate a submission cover letter",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "journal_name": {"type": "string"},
                        "editor_name": {"type": "string"},
                        "paper_title": {"type": "string"},
                        "key_contributions": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["journal_name", "paper_title"],
                },
            },
            {
                "name": "respond_to_reviewers",
                "description": "Draft responses to peer reviewer comments",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "reviewer_comments": {"type": "string"},
                        "manuscript_context": {"type": "string"},
                    },
                    "required": ["reviewer_comments"],
                },
            },
        ]

    def prepare_submission(self, paper_title: str, abstract: str,
                            target_journal: str) -> str:
        return self.run(
            task=f"""Prepare complete submission package for:

Paper Title: {paper_title}
Target Journal: {target_journal}
Abstract:
{abstract}

Produce complete submission package:
1. Pre-submission checklist (✓/✗ per item with notes)
2. Journal author guidelines summary (based on known guidelines)
3. Cover letter (complete, ready to send)
4. Suggested reviewers (5 names with justification + no-conflict confirmation)
5. Keywords list (6-8 terms optimized for discoverability)
6. Highlights (3-5 bullets, ≤85 chars each, for Elsevier submission)
7. Author contribution statement (CRediT taxonomy)
8. Data availability statement template
9. Ethics declaration template (Thai IRB + PDPA)
10. Expected review timeline and contingency plan (desk reject → next journal)""",
            artifact_type="submission_package",
            artifact_title=f"Submission Package: {paper_title[:60]}",
        )

    def respond_to_reviews(self, reviewer_comments: str, paper_summary: str) -> str:
        return self.run(
            task=f"""Draft a professional peer review response for:

Paper Summary: {paper_summary}

Reviewer Comments:
{reviewer_comments}

Generate:
1. Response letter opening (to editor)
2. Point-by-point responses to ALL reviewer comments:
   - Reviewer 1: Comment → Response → Change made (with line numbers)
   - Reviewer 2: Comment → Response → Change made
3. Summary of changes table
4. Closing statement to editor
5. Recommendation: revise & resubmit vs. appeal vs. submit elsewhere""",
            artifact_type="review_response",
            artifact_title="Peer Review Response Letter",
        )
