from fastapi import APIRouter, HTTPException
from app.models.research import LiteratureSearchRequest, LiteratureSearchResponse
import httpx
from typing import List, Optional

router = APIRouter()


@router.post("/search", response_model=LiteratureSearchResponse)
async def search_literature(request: LiteratureSearchRequest):
    papers = await _search_semantic_scholar(
        query=f"aviation {request.query}",
        limit=request.limit,
        year_from=request.year_from,
        year_to=request.year_to,
    )

    return LiteratureSearchResponse(
        papers=papers,
        total=len(papers),
        thematic_summary=f"Found {len(papers)} papers related to {request.query} in aviation domain",
        key_trends=["Digital transformation", "AI adoption", "Sustainability", "Safety management"],
        suggested_gaps=["Limited studies on post-COVID recovery", "Need for multi-country comparisons"],
    )


async def _search_semantic_scholar(query: str, limit: int = 20, year_from: int = 2015, year_to: int = 2024) -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params={
                    "query": query,
                    "limit": limit,
                    "fields": "title,authors,year,abstract,citationCount,externalIds",
                    "publicationDateOrYear": f"{year_from}-{year_to}",
                },
                timeout=30.0,
            )
            data = response.json()
            return data.get("data", [])
        except Exception:
            return []


@router.get("/trends/{domain}")
async def get_research_trends(domain: str):
    return {
        "domain": domain,
        "top_journals": [
            "Journal of Air Transport Management",
            "Transportation Research Part A",
            "Journal of Aviation/Aerospace Education & Research",
            "International Journal of Aviation Management",
        ],
        "trending_topics": [
            "Digital transformation in aviation",
            "Sustainable aviation fuel adoption",
            "Post-COVID passenger recovery",
            "AI in air traffic management",
        ],
        "citation_metrics": {
            "h_index_avg": 12,
            "citations_avg": 45,
            "papers_per_year": 234,
        },
    }
