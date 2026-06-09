from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class JournalMatchRequest(BaseModel):
    title: str
    abstract: str
    keywords: List[str]
    domain: str = "aviation"


@router.post("/journal-match")
async def match_journals(request: JournalMatchRequest):
    return {
        "recommended_journals": [
            {
                "name": "Journal of Air Transport Management",
                "publisher": "Elsevier",
                "impact_factor": 4.2,
                "quartile": "Q1",
                "indexed": ["Scopus", "WoS"],
                "match_score": 0.92,
                "submission_url": "https://www.journals.elsevier.com/journal-of-air-transport-management",
            },
            {
                "name": "Transportation Research Part A",
                "publisher": "Elsevier",
                "impact_factor": 5.3,
                "quartile": "Q1",
                "indexed": ["Scopus", "WoS"],
                "match_score": 0.85,
                "submission_url": "https://www.journals.elsevier.com/transportation-research-part-a",
            },
            {
                "name": "Journal of Air Transport Studies",
                "publisher": "ATRC",
                "impact_factor": 1.8,
                "quartile": "Q2",
                "indexed": ["Scopus"],
                "match_score": 0.78,
                "submission_url": "",
            },
        ]
    }


@router.post("/cover-letter")
async def generate_cover_letter(
    title: str,
    abstract: str,
    journal_name: str,
    author_names: List[str],
):
    return {
        "cover_letter": f"""Dear Editor,

We are pleased to submit our manuscript entitled "{title}" for consideration for publication in {journal_name}.

This manuscript has not been published elsewhere and is not under consideration by another journal.

{abstract[:200]}...

We believe this work makes a significant contribution to the field of aviation management research and will be of interest to your readers.

Sincerely,
{', '.join(author_names)}"""
    }
