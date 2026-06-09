"""
Aviation Research Agent Platform — Demo Entry Point
Demonstrates all five specialized research agents working as a team.
"""
import os
import sys

# ── Quick demo (no real API call) when ANTHROPIC_API_KEY is not set ──────────
DEMO_MODE = not os.environ.get("ANTHROPIC_API_KEY")

if DEMO_MODE:
    print("="*70)
    print("  AVIATION RESEARCH AGENT PLATFORM — Architecture Demo")
    print("="*70)
    print()
    print("NOTE: Running in demo mode (ANTHROPIC_API_KEY not set).")
    print("Set the env var to run live agent calls.\n")
    print("PLATFORM ARCHITECTURE")
    print("─"*50)
    print("""
    User / Researcher
          │
          ▼
  ┌─────────────────────────────────────┐
  │  Aviation Research Orchestrator     │  ← Central intelligence
  │  (Research Companion pattern)       │    routes + synthesizes
  └──┬──────┬───────┬──────┬────────────┘
     │      │       │      │       │
  ┌──▼──┐ ┌─▼──┐ ┌──▼─┐ ┌─▼──┐ ┌──▼────┐
  │ Lit │ │Quest│ │ SEM│ │ APA│ │Thesis │
  │ Rev │ │naire│ │Anal│ │ Ref│ │Review │
  │Agent│ │Agent│ │yst │ │Agt │ │ Agent │
  └─────┘ └─────┘ └────┘ └────┘ └───────┘
          │
  ┌───────▼─────────────────────────────┐
  │  Research Memory (Total Recall)     │  ← Long-horizon persistent
  │  Message Bus (Agent-to-Agent)       │    state (Orchestra pattern)
  └─────────────────────────────────────┘
""")
    print("REGISTERED AGENTS")
    print("─"*50)
    agents = [
        ("Literature Review Agent",    "Survey papers, map frontiers, identify gaps"),
        ("Questionnaire Design Agent", "Design validated survey instruments (NASA-TLX, SHELL, CRM)"),
        ("SEM Analysis Agent",         "CB-SEM / PLS-SEM / CFA / mediation analysis"),
        ("APA Reference Agent",        "APA 7th edition formatting + ICAO/FAA/EASA documents"),
        ("Thesis Reviewer Agent",      "Chapter review, viva prep, alignment check"),
    ]
    for name, role in agents:
        print(f"  ✓ {name}")
        print(f"    → {role}")
    print()
    print("SAMPLE RESEARCH PIPELINE")
    print("─"*50)
    print("  RQ: How does safety culture affect incident reporting in Thai airlines?")
    print()
    print("  [1] Literature Review Agent")
    print("      → Identifies: Reason, Reason (1990); Wiegmann & Shappell (2003);")
    print("        HFACS framework; Thai aviation safety literature gap")
    print()
    print("  [2] Questionnaire Design Agent")
    print("      → Constructs: Safety Culture, Just Culture, Reporting Intention")
    print("        Items: 24 items, 5-point Likert, back-translated TH/EN")
    print()
    print("  [3] SEM Analysis Agent")
    print("      → PLS-SEM (n=186): Safety Culture → Just Culture → Reporting")
    print("        AVE > 0.50, HTMT < 0.85, R² = 0.61")
    print()
    print("  [4] APA Reference Agent")
    print("      → Formats 35 references including ICAO Annex 13 (2016)")
    print("        and FAA AC 120-117 in APA 7th edition")
    print()
    print("  [5] Thesis Reviewer Agent")
    print("      → Chapter 3 score: 8/10 | Revisions: 3 items")
    print("        Viva Q: 'Justify PLS-SEM over CB-SEM for n=186'")
    print()
    print("="*70)
    print("  Set ANTHROPIC_API_KEY and re-run for live agent execution.")
    print("="*70)
    sys.exit(0)

# ── Live mode ─────────────────────────────────────────────────────────────────
from aviation_research_platform import AviationResearchOrchestrator

def interactive_mode():
    """Run the platform in interactive chat mode (like Orchestra's Research IDE)."""
    platform = AviationResearchOrchestrator()
    print("Aviation Research Agent Platform — Interactive Mode")
    print("Type 'exit' to quit, 'pipeline' to run a full research pipeline demo.\n")

    while True:
        user_input = input("Researcher: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Session saved. Goodbye!")
            break
        if user_input.lower() == "pipeline":
            run_pipeline_demo(platform)
            continue

        response = platform.chat(user_input)
        print(f"\nOrchestra ARA:\n{response}\n")


def run_pipeline_demo(platform=None):
    """Run the full aviation research pipeline on a sample research question."""
    if platform is None:
        platform = AviationResearchOrchestrator()

    results = platform.run_full_research_pipeline(
        research_question=(
            "How does safety culture influence incident reporting behavior "
            "among commercial airline pilots in Thailand?"
        ),
        topic="Aviation Safety Culture and Incident Reporting",
        constructs=["Safety_Culture", "Just_Culture", "Psychological_Safety", "Reporting_Intention"],
        target_population="Commercial airline pilots holding ATPL, based in Thailand, n≥200",
        sample_size=220,
    )

    print("\n" + "="*60)
    print("PIPELINE RESULTS SUMMARY")
    print("="*60)
    for section, content in results.items():
        print(f"\n--- {section.upper().replace('_', ' ')} ---")
        print(content[:500] + "..." if len(content) > 500 else content)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pipeline":
        run_pipeline_demo()
    else:
        interactive_mode()
