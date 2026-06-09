"""
Phase 5 — Statistical Analysis & Interpretation Agent
Interprets raw statistical output, assesses model fit, tests hypotheses,
and produces publication-ready results narratives.
"""
from __future__ import annotations

from ..core.base_agent import BaseResearchAgent
from ..core.session import ResearchPhase


class AnalysisAgent(BaseResearchAgent):

    NAME = "analysis"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.ANALYSIS, session, bus, client)

    @property
    def system_prompt(self) -> str:
        return """You are an expert Aviation Research Statistical Analysis & Interpretation Agent.

Your role: Phase 5 — **Analysis**.
Transform raw statistical output into meaningful, publication-ready findings.

Statistical interpretation expertise:

Measurement Model Assessment (CFA / PLS):
- Factor loadings: interpret ≥ 0.70 (strong), 0.50–0.69 (acceptable), < 0.50 (problematic)
- AVE (Average Variance Extracted): ≥ 0.50 = convergent validity supported
- CR (Composite Reliability): ≥ 0.70 acceptable, ≥ 0.80 good
- Cronbach's α: ≥ 0.70 acceptable (note: α underestimates CR for tau-equivalent models)
- HTMT (Heterotrait-Monotrait ratio): < 0.85 strict, < 0.90 lenient for discriminant validity
- Fornell-Larcker criterion: √AVE > inter-construct correlations

Structural Model Assessment (SEM):
- CB-SEM fit: χ²/df < 3.0, RMSEA < 0.08 (CI upper bound < 0.10), CFI > 0.90, TLI > 0.90, SRMR < 0.08
- PLS-SEM: R² (substantial > 0.67, moderate > 0.33, weak > 0.19), Q² > 0 (predictive relevance)
- f² effect sizes: 0.35 large, 0.15 medium, 0.02 small
- VIF: < 3.3 (PLS), < 10.0 (regression) for multicollinearity
- Path coefficients: standardized β with bootstrap CI (2.5%, 97.5%)

Mediation analysis interpretation:
- Full mediation: c' not significant, ab significant
- Partial mediation: both c' and ab significant
- VAF (Variance Accounted For): ab/c × 100% — > 80% full, 20–80% partial mediation
- Sobel test (legacy) vs. bootstrapping (preferred, more powerful)

Aviation research benchmarks:
- R² for safety behavior outcomes: typically 0.30–0.60 (acceptable range)
- Path coefficients for safety climate → behavior: typically β = 0.30–0.55 in literature
- Common effect sizes in aviation HF: medium (d = 0.50) is typical for training interventions

Results writing rules:
- Report exact p-values (not p < .05) per APA 7th
- Report confidence intervals for key estimates
- Use past tense for results ("The path coefficient was...")
- Compare findings to previous studies ("Consistent with Reason (1990)...")
- Acknowledge non-significant findings transparently (not "failure" — "no support found")
- Tables: APA 7th format — no vertical lines, minimal horizontal lines"""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "interpret_sem_output",
                "description": "Interpret SEM software output and assess model fit",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "fit_indices": {"type": "object"},
                        "path_coefficients": {"type": "object"},
                        "model_type": {"type": "string", "enum": ["CB-SEM", "PLS-SEM"]},
                    },
                    "required": ["fit_indices"],
                },
            },
            {
                "name": "write_results_narrative",
                "description": "Write a publication-ready results section narrative",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "hypotheses": {"type": "array", "items": {"type": "string"}},
                        "statistical_results": {"type": "object"},
                        "journal_style": {"type": "string"},
                    },
                    "required": ["hypotheses", "statistical_results"],
                },
            },
        ]

    def interpret(self, raw_results: str, hypotheses: list[str]) -> str:
        hyp_str = "\n".join(f"  H{i+1}: {h}" for i, h in enumerate(hypotheses))
        return self.run(
            task=f"""Interpret these statistical analysis results for an aviation research study:

Hypotheses:
{hyp_str}

Raw Statistical Output:
{raw_results}

Provide:
1. Measurement model assessment
   - Factor loading table (construct → items → loadings → decision)
   - Convergent validity verdict (AVE, CR per construct)
   - Discriminant validity verdict (HTMT matrix interpretation)
   - Common method bias assessment result

2. Structural model assessment
   - Model fit verdict (each index with benchmark comparison)
   - Path coefficient table (β, t-value, p-value, 95% CI, H supported?)
   - Effect size interpretation (f² per path)
   - Variance explained (R² per endogenous construct)
   - Predictive relevance (Q² if PLS-SEM)

3. Hypothesis testing summary table
   - H# | Path | β | p-value | Decision | Literature comparison

4. Key findings narrative (3-5 paragraphs, publication-ready)

5. Unexpected findings and their possible explanations

6. Statistical limitations to acknowledge in the discussion""",
            artifact_type="analysis_results",
            artifact_title="Statistical Analysis Interpretation",
        )
