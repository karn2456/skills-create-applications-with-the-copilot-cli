from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class ResearchStatus(str, Enum):
    IDEATION = "ideation"
    LITERATURE = "literature"
    FRAMEWORK = "framework"
    QUESTIONNAIRE = "questionnaire"
    DATA_COLLECTION = "data-collection"
    ANALYSIS = "analysis"
    WRITING = "writing"
    PUBLICATION = "publication"


class AviationDomain(str, Enum):
    AIRLINE = "airline"
    AIRPORT = "airport"
    CARGO = "cargo"
    SAFETY = "safety"
    TECHNOLOGY = "technology"
    SUSTAINABILITY = "sustainability"
    PASSENGER = "passenger"
    ECONOMICS = "economics"
    LOGISTICS = "logistics"
    GROUND_HANDLING = "ground_handling"


class TopicGenerationRequest(BaseModel):
    domain: AviationDomain
    research_level: str = Field(..., description="master, phd, dba")
    keywords: Optional[List[str]] = None
    preferred_theory: Optional[str] = None
    language: str = "en"


class TopicGenerationResponse(BaseModel):
    topics: List[dict]
    gaps: List[str]
    recommendations: str
    domain_context: str


class LiteratureSearchRequest(BaseModel):
    query: str
    domain: Optional[AviationDomain] = None
    year_from: Optional[int] = 2015
    year_to: Optional[int] = 2024
    sources: List[str] = ["semantic_scholar", "crossref"]
    limit: int = 20


class LiteratureSearchResponse(BaseModel):
    papers: List[dict]
    total: int
    thematic_summary: str
    key_trends: List[str]
    suggested_gaps: List[str]


class FrameworkRequest(BaseModel):
    research_title: str
    domain: AviationDomain
    independent_variables: List[str]
    dependent_variables: List[str]
    theory: str
    include_mediators: bool = True
    include_moderators: bool = False


class FrameworkResponse(BaseModel):
    framework_description: str
    variables: dict
    hypotheses: List[str]
    theory_justification: str
    diagram_data: dict


class QuestionnaireRequest(BaseModel):
    research_title: str
    constructs: List[dict]
    scale_points: int = 5
    language: str = "both"
    include_demographics: bool = True


class QuestionnaireResponse(BaseModel):
    questionnaire: dict
    items_count: int
    sections: List[dict]
    validity_notes: str


class AnalysisRequest(BaseModel):
    data_description: str
    sample_size: int
    method: str
    constructs: List[str]
    hypotheses: List[str]
    software: str = "jamovi"


class AnalysisResponse(BaseModel):
    results_interpretation: str
    tables: List[dict]
    charts: List[dict]
    apa_report: str
    recommendations: str


class AgentChatRequest(BaseModel):
    agent_id: str
    message: str
    context: Optional[dict] = None
    project_id: Optional[str] = None
    language: str = "th"


class AgentChatResponse(BaseModel):
    response: str
    agent_id: str
    suggestions: List[str]
    next_steps: List[str]
    artifacts: Optional[List[dict]] = None
