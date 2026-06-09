"""
P1-001 FIX: Real Literature Search APIs
=========================================
แทนที่ LLM simulation ด้วย API จริง (ทั้งหมดฟรี):

API ที่ใช้:
  1. Semantic Scholar API  — https://api.semanticscholar.org  (free, 100 req/5min)
  2. CrossRef API          — https://api.crossref.org         (free, polite pool)
  3. arXiv API             — https://export.arxiv.org/api     (free, XML)
  4. OpenAlex API          — https://api.openalex.org         (free, replaces MAG)

สำหรับ SCOPUS (ต้องมี institutional license):
  - Elsevier Developer Portal: https://dev.elsevier.com
  - ใช้ APIKEY จากสถาบัน (ม.มหิดล, จุฬา, NIDA มักมี)

Install: pip install httpx
"""
from __future__ import annotations

import httpx
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any


@dataclass
class Paper:
    title: str
    authors: list[str]
    year: int | None
    abstract: str
    doi: str | None
    url: str | None
    citation_count: int = 0
    source: str = ""

    def to_apa(self) -> str:
        """Format as APA 7th edition reference."""
        author_str = _format_apa_authors(self.authors)
        year = f"({self.year})" if self.year else "(n.d.)"
        doi_str = f" https://doi.org/{self.doi}" if self.doi else ""
        return f"{author_str} {year}. {self.title}.{doi_str}"


def _format_apa_authors(authors: list[str]) -> str:
    if not authors:
        return "Unknown Author."
    formatted = []
    for a in authors[:20]:
        parts = a.strip().split()
        if len(parts) >= 2:
            last = parts[-1]
            initials = ". ".join(p[0] for p in parts[:-1]) + "."
            formatted.append(f"{last}, {initials}")
        else:
            formatted.append(a)
    if len(authors) > 20:
        formatted.append("...")
        formatted.append(_format_apa_authors([authors[-1]]))
        return "; ".join(formatted[:-2]) + f"; ... {formatted[-1]}"
    if len(formatted) == 1:
        return formatted[0]
    return "; ".join(formatted[:-1]) + f", & {formatted[-1]}"


# ─────────────────────────────────────────────────────────────
# 1. Semantic Scholar (best for aviation HF — covers ACM, IEEE, Elsevier)
# ─────────────────────────────────────────────────────────────

class SemanticScholarClient:
    BASE = "https://api.semanticscholar.org/graph/v1"
    FIELDS = "title,authors,year,abstract,externalIds,citationCount,openAccessPdf"

    def __init__(self, api_key: str | None = None):
        headers = {"x-api-key": api_key} if api_key else {}
        self.http = httpx.Client(headers=headers, timeout=30.0)

    def search(self, query: str, limit: int = 20,
               year_range: str | None = None) -> list[Paper]:
        """
        query: "safety culture incident reporting aviation"
        year_range: "2015-2025"
        """
        params: dict[str, Any] = {
            "query": query,
            "limit": limit,
            "fields": self.FIELDS,
        }
        if year_range:
            params["year"] = year_range

        resp = self.http.get(f"{self.BASE}/paper/search", params=params)
        resp.raise_for_status()
        data = resp.json()

        papers = []
        for item in data.get("data", []):
            papers.append(Paper(
                title=item.get("title", ""),
                authors=[a.get("name", "") for a in item.get("authors", [])],
                year=item.get("year"),
                abstract=item.get("abstract") or "",
                doi=item.get("externalIds", {}).get("DOI"),
                url=(item.get("openAccessPdf") or {}).get("url"),
                citation_count=item.get("citationCount", 0),
                source="Semantic Scholar",
            ))
        return papers

    def get_paper_details(self, paper_id: str) -> dict:
        """Get detailed info including references and citations."""
        resp = self.http.get(
            f"{self.BASE}/paper/{paper_id}",
            params={"fields": self.FIELDS + ",references,citations"},
        )
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self.http.close()


# ─────────────────────────────────────────────────────────────
# 2. CrossRef (DOI resolution, journal metadata, citation counts)
# ─────────────────────────────────────────────────────────────

class CrossRefClient:
    BASE = "https://api.crossref.org/works"

    def __init__(self, email: str = "research@example.com"):
        # Polite pool: provide email in User-Agent for better rate limits
        self.http = httpx.Client(
            headers={"User-Agent": f"AviationResearchOS/1.0 (mailto:{email})"},
            timeout=30.0,
        )

    def search(self, query: str, limit: int = 20,
               filter_issn: str | None = None) -> list[Paper]:
        params: dict[str, Any] = {
            "query": query,
            "rows": limit,
            "sort": "relevance",
            "select": "DOI,title,author,published,abstract,is-referenced-by-count",
        }
        if filter_issn:
            params["filter"] = f"issn:{filter_issn}"  # e.g., "0001-4575" = AAP

        resp = self.http.get(self.BASE, params=params)
        resp.raise_for_status()
        items = resp.json().get("message", {}).get("items", [])

        papers = []
        for item in items:
            title = ""
            if isinstance(item.get("title"), list):
                title = item["title"][0] if item["title"] else ""

            authors = []
            for a in item.get("author", []):
                given = a.get("given", "")
                family = a.get("family", "")
                authors.append(f"{given} {family}".strip())

            pub_date = item.get("published", {})
            year = None
            if pub_date.get("date-parts"):
                parts = pub_date["date-parts"][0]
                year = parts[0] if parts else None

            abstract_raw = item.get("abstract", "")
            # CrossRef wraps abstract in <jats:p> tags
            abstract = ET.fromstring(f"<r>{abstract_raw}</r>").text or "" \
                if abstract_raw and "<" in abstract_raw else abstract_raw

            papers.append(Paper(
                title=title,
                authors=authors,
                year=year,
                abstract=abstract[:500],
                doi=item.get("DOI"),
                url=f"https://doi.org/{item['DOI']}" if item.get("DOI") else None,
                citation_count=item.get("is-referenced-by-count", 0),
                source="CrossRef",
            ))
        return papers

    def close(self):
        self.http.close()


# ─────────────────────────────────────────────────────────────
# 3. arXiv (AI in aviation, drone research, ML for aviation safety)
# ─────────────────────────────────────────────────────────────

class ArXivClient:
    BASE = "https://export.arxiv.org/api/query"
    NS = {"atom": "http://www.w3.org/2005/Atom"}

    def __init__(self):
        self.http = httpx.Client(timeout=30.0)

    def search(self, query: str, limit: int = 10,
               categories: list[str] | None = None) -> list[Paper]:
        """
        categories: ["cs.AI", "cs.LG", "eess.SY"] for aviation AI
        query: "aviation safety machine learning"
        """
        search_query = query
        if categories:
            cat_filter = " OR ".join(f"cat:{c}" for c in categories)
            search_query = f"({query}) AND ({cat_filter})"

        resp = self.http.get(self.BASE, params={
            "search_query": f"all:{search_query}",
            "max_results": limit,
            "sortBy": "relevance",
        })
        resp.raise_for_status()

        root = ET.fromstring(resp.text)
        papers = []
        for entry in root.findall("atom:entry", self.NS):
            title = (entry.findtext("atom:title", "", self.NS) or "").strip()
            abstract = (entry.findtext("atom:summary", "", self.NS) or "").strip()
            authors = [
                (a.findtext("atom:name", "", self.NS) or "").strip()
                for a in entry.findall("atom:author", self.NS)
            ]
            published = entry.findtext("atom:published", "", self.NS) or ""
            year = int(published[:4]) if published else None
            url = entry.findtext("atom:id", "", self.NS) or ""

            papers.append(Paper(
                title=title,
                authors=authors,
                year=year,
                abstract=abstract[:500],
                doi=None,
                url=url,
                source="arXiv",
            ))
        return papers

    def close(self):
        self.http.close()


# ─────────────────────────────────────────────────────────────
# 4. HOW TO WIRE INTO LiteratureSearchAgent
# ─────────────────────────────────────────────────────────────

INTEGRATION_EXAMPLE = '''
# In literature_search_agent.py — add real tool executors:

from aviation_research_platform.fixes.p1_real_search_apis import (
    SemanticScholarClient, CrossRefClient, ArXivClient
)

class LiteratureSearchAgent(BaseResearchAgent):

    def __init__(self, session, bus, client):
        super().__init__(...)
        self._ss = SemanticScholarClient()
        self._cr = CrossRefClient(email="researcher@university.ac.th")
        self._ax = ArXivClient()

    def _get_tool_executors(self):
        return {
            "database_search": self._exec_database_search,
            "build_search_string": self._exec_build_string,
        }

    def _exec_database_search(self, database: str, search_string: str,
                              filters: dict | None = None) -> str:
        filters = filters or {}
        year_range = filters.get("year_range", "2010-2026")

        if database in ("SCOPUS", "Web_of_Science", "generic"):
            papers = self._ss.search(search_string, limit=25, year_range=year_range)
        elif database == "CrossRef":
            papers = self._cr.search(search_string, limit=25)
        elif database == "arXiv":
            papers = self._ax.search(search_string, limit=15)
        else:
            papers = self._ss.search(search_string, limit=20)

        # Format for LLM consumption
        lines = [f"Found {len(papers)} papers for: {search_string}\\n"]
        for i, p in enumerate(papers, 1):
            lines.append(
                f"{i}. {p.title} ({p.year or 'n.d.'}) | "
                f"Cited: {p.citation_count} | Source: {p.source}"
            )
            if p.abstract:
                lines.append(f"   Abstract: {p.abstract[:150]}...")
        return "\\n".join(lines)

    def _exec_build_string(self, keywords: list[str],
                          database_syntax: str = "generic") -> str:
        terms = '" AND "'.join(keywords)
        if database_syntax == "SCOPUS":
            return f\'TITLE-ABS-KEY("{terms}")\'
        return f\'("{terms}")\'
'''
