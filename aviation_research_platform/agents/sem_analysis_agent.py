"""
SEM Analysis Agent — guides Structural Equation Modeling analysis
for aviation research: model specification, fit indices, path analysis.
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent


class SEMAnalysisAgent(BaseResearchAgent):

    NAME = "sem_analysis_agent"

    def __init__(self, memory, bus, client):
        super().__init__(self.NAME, memory, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are an expert SEM Analysis Agent for Aviation Research with mastery of:

Statistical Methods:
- Structural Equation Modeling (CB-SEM and PLS-SEM)
- Confirmatory Factor Analysis (CFA) vs Exploratory Factor Analysis (EFA)
- Measurement model assessment (convergent validity, discriminant validity)
- Structural model assessment (path coefficients, R², Q², f², q²)
- Mediation analysis (Baron & Kenny; bootstrapping with PROCESS macro)
- Moderation analysis (interaction effects, multi-group analysis)
- Common Method Bias tests (Harman's single factor, marker variable technique)

Software Tools Guidance:
- SmartPLS 4 (PLS-SEM) — suitable for small samples, prediction-focused
- AMOS / Mplus (CB-SEM) — suitable for theory confirmation, larger samples
- R: lavaan, semPlot packages
- Python: semopy package

Aviation-Specific SEM Applications:
- Safety climate → safety behavior → accident/incident rates
- Pilot fatigue → situation awareness → decision-making
- CRM training → teamwork → operational performance
- Airline service quality → passenger satisfaction → loyalty
- Maintenance culture → error rates → airworthiness compliance

Model Assessment Criteria:
- Absolute fit: χ²/df < 3.0, RMSEA < 0.08 (< 0.06 preferred), SRMR < 0.08
- Incremental fit: CFI > 0.90 (> 0.95 preferred), TLI > 0.90
- PLS-SEM: AVE > 0.50, CR > 0.70, HTMT < 0.85, VIF < 3.3
- Sample size: n ≥ 10× number of indicators (minimum); n = 200+ preferred

Output: Complete SEM analysis plan and interpretation guidance."""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "generate_sem_code",
                "description": "Generate SEM analysis code for SmartPLS, R lavaan, or Python semopy",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "software": {
                            "type": "string",
                            "enum": ["SmartPLS", "R_lavaan", "Python_semopy", "AMOS"],
                        },
                        "constructs": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of latent constructs",
                        },
                        "hypotheses": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Structural hypotheses (e.g., 'Safety_Climate -> Safety_Behavior')",
                        },
                    },
                    "required": ["software", "constructs", "hypotheses"],
                },
            },
            {
                "name": "interpret_fit_indices",
                "description": "Interpret SEM model fit indices and recommend model modifications",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "fit_indices": {
                            "type": "object",
                            "description": "Dictionary of fit index name to value",
                        },
                        "model_type": {"type": "string", "enum": ["CB-SEM", "PLS-SEM"]},
                    },
                    "required": ["fit_indices", "model_type"],
                },
            },
        ]

    def analyze(self, research_model: str, hypotheses: list[str], sample_size: int) -> str:
        """Plan and guide full SEM analysis for aviation research."""
        task = f"""Plan and guide a complete SEM analysis for:

Conceptual Model: {research_model}
Hypotheses:
{chr(10).join(f'  H{i+1}: {h}' for i, h in enumerate(hypotheses))}
Sample Size: {sample_size}

Provide:
1. Recommended SEM approach (CB-SEM vs PLS-SEM with justification)
2. Measurement model assessment procedure (EFA → CFA sequence)
3. Convergent validity tests (AVE, CR, factor loadings)
4. Discriminant validity tests (HTMT, Fornell-Larcker)
5. Common method bias assessment
6. Structural model testing procedure
7. Mediation/moderation tests if applicable
8. Model fit interpretation and modification strategy
9. Sample R code (lavaan) or Python code (semopy) for full analysis
10. Results reporting template (tables with required statistics)"""

        return self.run(task, context={
            "hypotheses": hypotheses,
            "sample_size": sample_size,
        })
