"""
Phase 4 — Code Execution Agent
Writes, explains, and simulates execution of research analysis code.
Covers: data cleaning, descriptive stats, SEM, regression, visualization.
In live mode: can execute Python directly using subprocess sandbox.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

from ..core.base_agent import BaseResearchAgent
from ..core.session import ResearchPhase


class CodeExecutionAgent(BaseResearchAgent):

    NAME = "code_execution"

    def __init__(self, session, bus, client, enable_execution: bool = False):
        super().__init__(self.NAME, ResearchPhase.EXECUTION, session, bus, client)
        self._enable_execution = enable_execution

    @property
    def system_prompt(self) -> str:
        return """You are an expert Aviation Research Code Execution Agent.

Your role: Phase 4 — **Execution**.
Write complete, runnable Python code for aviation research data analysis.

You orchestrate the full data pipeline:

Data Ingestion & Cleaning:
- Read survey CSV exports from Google Forms / Qualtrics / SurveyMonkey
- Handle missing values: MCAR/MAR/MNAR diagnosis, listwise vs. multiple imputation
- Detect and handle outliers: Mahalanobis distance (multivariate), z-score
- Reverse-code negatively worded items
- Compute composite scores (mean/sum per construct)
- Data format: reshape wide ↔ long, merge datasets

Descriptive Statistics:
- Respondent profile tables (demographic breakdown)
- Mean, SD, skewness, kurtosis per construct
- Correlation matrix (Pearson, Spearman for ordinal)
- Frequency and percentage for categorical variables

Reliability & Validity:
- Cronbach's alpha (using pingouin or reliability_analysis)
- Item-total correlations (flag items < 0.30)
- Exploratory Factor Analysis (factor_analyzer, sklearn decomposition)
- Confirmatory Factor Analysis (semopy, lavaan via rpy2)

Structural Equation Modeling:
- PLS-SEM: custom implementation or SmartPLS export interpretation
- CB-SEM: semopy (Python) or lavaan (R via subprocess)
- Fit indices: χ²/df, RMSEA, CFI, TLI, SRMR, AIC, BIC
- Path coefficients, t-values, p-values, confidence intervals
- Bootstrapping for mediation analysis (5000 iterations)

Visualization:
- matplotlib / seaborn: path diagrams, correlation heatmaps
- plotly: interactive results for presentation
- Path diagram drawing using networkx + matplotlib

Libraries assumed available:
pandas, numpy, scipy, sklearn, semopy, pingouin, matplotlib, seaborn,
factor_analyzer, statsmodels, networkx

Code standards:
- Type hints on all functions
- Docstring on each function (1 line)
- Reproducible: set random seeds
- Commented sections for teaching/thesis documentation
- Output: print clear results tables with interpretation guidance
- Save all outputs to /results/ directory"""

    def tools(self) -> list[dict]:
        return [
            {
                "name": "execute_python",
                "description": "Execute a Python code snippet and return stdout/stderr",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Python code to execute"},
                        "timeout": {"type": "integer", "default": 30},
                    },
                    "required": ["code"],
                },
            },
        ]

    def generate_analysis_code(self, analysis_type: str, constructs: list[str],
                                hypotheses: list[str]) -> str:
        constructs_str = ", ".join(constructs)
        hyp_str = "\n".join(f"  {h}" for h in hypotheses)
        return self.run(
            task=f"""Write complete Python analysis code for:

Analysis Type: {analysis_type}
Constructs: {constructs_str}
Hypotheses:
{hyp_str}

Generate a complete, runnable Python script with these sections:

# ── Section 1: Imports & Configuration ──
# ── Section 2: Data Loading & Cleaning ──
# ── Section 3: Descriptive Statistics ──
# ── Section 4: Reliability Analysis (Cronbach's α) ──
# ── Section 5: Validity Assessment (EFA / CFA) ──
# ── Section 6: Common Method Bias Test (Harman's single factor) ──
# ── Section 7: Structural Model (SEM / Regression) ──
# ── Section 8: Hypothesis Testing Results Table ──
# ── Section 9: Mediation Analysis (if applicable) ──
# ── Section 10: Visualization ──
# ── Section 11: Export Results to /results/ ──

Include:
- Sample data generation (so the code runs without a real dataset)
- Interpretation guidelines as comments
- How to replace sample data with real survey CSV""",
            artifact_type="analysis_code",
            artifact_title=f"Analysis Code: {analysis_type}",
        )

    def execute_code(self, code: str, timeout: int = 30) -> dict:
        """Actually run Python code in a sandboxed subprocess. Returns stdout/stderr/exit_code."""
        if not self._enable_execution:
            return {
                "stdout": "[Execution disabled — set enable_execution=True to run code]",
                "stderr": "",
                "exit_code": 0,
            }
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(code)
            tmp_path = f.name
        try:
            result = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True, text=True, timeout=timeout,
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": "Execution timed out.", "exit_code": -1}
        finally:
            Path(tmp_path).unlink(missing_ok=True)
