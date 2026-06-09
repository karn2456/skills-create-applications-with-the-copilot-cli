"""
Questionnaire Design Agent — designs validated survey instruments
for aviation research, grounded in established scales and best practices.
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent
from ..core.session import ResearchPhase


class QuestionnaireDesignAgent(BaseResearchAgent):

    NAME = "questionnaire_design"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.DESIGN, session, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are an expert Aviation Research Questionnaire Design Agent with deep expertise in:
- Psychometric scale development (CTT and IRT frameworks)
- Aviation-specific validated instruments:
  * NASA-TLX (Task Load Index for pilot workload)
  * SHELL Model questionnaires
  * FMAQ (Flight Management Attitudes Questionnaire)
  * SART (Situational Awareness Rating Technique)
  * CRM Assessment Surveys (LOSA, TEM)
  * Safety Climate surveys (Manchester Patient Safety Framework adapted for aviation)
  * Job Satisfaction and Organizational Commitment scales for aviation workers
- Likert, semantic differential, and forced-choice scale design
- Survey validity (content, construct, criterion) and reliability (Cronbach's α, test-retest)
- Questionnaire translation protocols (back-translation for multilingual aviation studies)
- Ethics in research: informed consent, anonymity, IRB/EC requirements
- Pilot testing and cognitive interviewing procedures

Design Principles:
1. Align items directly to latent constructs from the theoretical framework
2. Reverse-code items to detect acquiescence bias
3. Avoid double-barreled, leading, and ambiguous items
4. Consider reading level (aviation maintenance vs. executive management respondents)
5. Optimize length: 20-40 items maximum for aviation operational personnel
6. Include demographic section relevant to aviation (license type, hours, airline, fleet, experience)

Output: Complete questionnaire with:
- Section headers and instructions
- All items with construct mapping
- Scoring guide
- Reliability targets (Cronbach's α ≥ 0.70)
- Validity evidence plan"""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "retrieve_validated_scale",
                "description": "Retrieve items from a validated aviation or organizational scale",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "scale_name": {"type": "string", "description": "Name of the validated scale"},
                        "construct": {"type": "string", "description": "Latent construct to measure"},
                    },
                    "required": ["construct"],
                },
            },
            {
                "name": "check_item_quality",
                "description": "Evaluate questionnaire items for clarity, bias, and alignment",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of questionnaire items to evaluate",
                        }
                    },
                    "required": ["items"],
                },
            },
        ]

    def design(self, research_question: str, constructs: list[str], target_population: str) -> str:
        """Design a complete questionnaire for aviation research."""
        task = f"""Design a complete research questionnaire for:

Research Question: {research_question}
Latent Constructs to Measure: {', '.join(constructs)}
Target Population: {target_population}

Deliverables:
1. Complete questionnaire (all sections, instructions, items)
2. Construct-item mapping table
3. Scoring and reverse-coding guide
4. Demographic section tailored to aviation context
5. Reliability and validity plan
6. Pilot testing procedure (5-10 respondents)
7. Estimated completion time"""

        return self.run(task, context={
            "constructs": constructs,
            "population": target_population,
        })
