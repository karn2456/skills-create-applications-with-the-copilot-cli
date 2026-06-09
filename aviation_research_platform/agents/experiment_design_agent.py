"""
Phase 3 — Experiment Design Agent
Designs the full research methodology: sampling, instrument, procedure, ethics.
Covers quantitative, qualitative, and mixed-methods approaches.
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent
from ..core.session import ResearchPhase


class ExperimentDesignAgent(BaseResearchAgent):

    NAME = "experiment_design"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.DESIGN, session, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are an expert Aviation Research Methodology & Experiment Design Agent.

Your role: Phase 3 — **Design**.
Translate research hypotheses into a rigorous, feasible research methodology.

Methodology expertise:

Quantitative designs:
- Cross-sectional survey (most common in aviation HF research)
- Longitudinal panel study (pre/post training, incident trend analysis)
- Quasi-experimental (simulator-based training interventions)
- Archival/secondary data (ASRS, AAIB, accident databases, ADS-B)
- Flight simulator experiments (controlled conditions, within-subjects)

Qualitative designs:
- Semi-structured interviews (pilots, controllers, maintenance engineers)
- Focus groups (flight deck crew, safety officers)
- Grounded theory (emerging phenomena: UAM adoption, new tech integration)
- Case study (single airline SMS implementation, accident investigation)
- Content analysis (incident reports, safety bulletins, CVRs where accessible)

Mixed-methods designs:
- Sequential explanatory: quantitative → qualitative to explain outliers
- Sequential exploratory: qualitative → quantitative to develop scales
- Concurrent triangulation: both simultaneously for convergent validity

Aviation sampling expertise:
- Thai aviation workforce: CAAT (Civil Aviation Authority Thailand) licensed personnel
- TCAS: ~3,500 ATPL holders, ~12,000 AMT, ~8,000 ATC/AFIS
- Access strategies: airline HR departments, AEROTHAI, CAAT training center
- Response rate benchmarks: online survey 20-35%; paper survey 60-80%
- Power analysis: G*Power for SEM (minimum n per free parameter rule: n = 5-10 × parameters)
- Stratified sampling by: airline type (LCC/FSC), fleet, role, experience band

Research ethics (Thai context):
- IRB/EC requirement: NIDA, Mahidol, Chulalongkorn ethics committees
- PDPA (Personal Data Protection Act B.E. 2562) compliance
- Aviation safety data protection: ICAO Annex 13 Section 5.12 protections
- Voluntary participation, right to withdraw, data anonymization

Instrument design guidance:
- Adapt validated scales (with permission) vs. develop new (higher bar)
- Back-translation procedure: English → Thai → English (independent translators)
- Pilot test: n=10-30 for cognitive interview + face validity
- Pre-test: n=30-50 for reliability estimates

Output: Complete methodology chapter blueprint."""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "power_analysis",
                "description": "Calculate required sample size using power analysis",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "analysis_type": {
                            "type": "string",
                            "enum": ["SEM", "regression", "ANOVA", "t_test", "correlation"],
                        },
                        "effect_size": {"type": "string", "enum": ["small", "medium", "large"]},
                        "alpha": {"type": "number", "default": 0.05},
                        "power": {"type": "number", "default": 0.80},
                        "num_predictors": {"type": "integer"},
                    },
                    "required": ["analysis_type"],
                },
            },
            {
                "name": "design_sampling_strategy",
                "description": "Design a sampling strategy for an aviation population",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "target_population": {"type": "string"},
                        "required_sample_size": {"type": "integer"},
                        "access_constraints": {"type": "string"},
                    },
                    "required": ["target_population"],
                },
            },
        ]

    def design(self, hypotheses: str, target_population: str, constraints: str = "") -> str:
        return self.run(
            task=f"""Design a complete research methodology for:

Hypotheses:
{hypotheses}

Target Population: {target_population}
Constraints: {constraints or "Standard Thai aviation research context"}

Deliver the complete methodology blueprint:

1. Research paradigm & philosophy (ontology, epistemology, axiology justification)
2. Research design selection (with rationale and alternative designs considered)
3. Population definition & sampling frame
4. Sample size calculation (G*Power parameters, justification)
5. Sampling strategy (simple random / stratified / purposive — with rationale)
6. Data collection instrument design brief
   - Variables → measures → scales → items count
   - Existing validated scales to adapt (with original citation)
   - New items to develop (if needed)
7. Data collection procedure (step-by-step, timeline, access strategy)
8. Pilot testing protocol
9. Ethics plan (PDPA compliance, IRB application checklist)
10. Data analysis plan (analytical techniques matched to each hypothesis)
11. Limitations anticipated (non-response bias, common method bias mitigation)
12. Timeline (Gantt chart in text form, weeks 1-52)""",
            artifact_type="research_design",
            artifact_title="Research Methodology Blueprint",
        )
