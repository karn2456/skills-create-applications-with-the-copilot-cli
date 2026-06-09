"""
Aviation Research OS — Entry Point

Modes:
  python main.py              → Architecture demo (no API key needed)
  python main.py chat         → Interactive research chat
  python main.py pipeline     → Full lifecycle demo
  python main.py status <id>  → Show session status
"""
import os
import sys


# ─────────────────────────────────────────────────────────────
#  DEMO MODE  (no ANTHROPIC_API_KEY required)
# ─────────────────────────────────────────────────────────────

def print_demo():
    W = 70
    def box(title):
        print("\n" + "─" * W)
        print(f"  {title}")
        print("─" * W)

    print("=" * W)
    print("  AVIATION RESEARCH OS — Architecture & Workflow Demo")
    print("  Inspired by Orchestra Research ARA")
    print("=" * W)

    # ── Architecture ──────────────────────────────────────────
    box("SYSTEM ARCHITECTURE")
    print("""
  ┌─────────────────────────────────────────────────────────┐
  │           Researcher (Human-in-the-Loop)                 │
  │         Propose → Curate → Supervise → Publish           │
  └────────────────────┬────────────────────────────────────┘
                       │ chat() / run_phase()
  ┌────────────────────▼────────────────────────────────────┐
  │           Aviation Research Orchestrator                  │
  │        Route → Execute → Synthesize → Remember           │
  └──┬──────┬──────┬───────┬───────┬───────┬────────────────┘
     │      │      │       │       │       │
  ┌──▼──┐ ┌─▼──┐ ┌▼────┐ ┌▼────┐ ┌▼────┐ ┌▼────────────┐
  │ Lit │ │Syn │ │ Gap │ │Exp  │ │Code │ │  Analysis   │
  │Srch │ │thes│ │Brain│ │Dsgn │ │Exec │ │  Writing    │
  │     │ │    │ │storm│ │Quest│ │     │ │  Pub/Thesis │
  └─────┘ └────┘ └─────┘ └─────┘ └─────┘ └─────────────┘
     │
  ┌──▼──────────────────────────────────────────────────────┐
  │  Research Session (Long-horizon Persistent State)        │
  │  • ResearchPhase tracking (7 phases)                     │
  │  • PhaseArtifacts (all outputs indexed)                  │
  │  • Dead-end registry (what didn't work)                  │
  │  • Research Knowledge Graph (papers/hypotheses/findings) │
  │  • Memory store (.research_sessions/<id>.json)           │
  └─────────────────────────────────────────────────────────┘
""")

    # ── Research OS vs Traditional ────────────────────────────
    box("RESEARCH OS vs TRADITIONAL WORKFLOW")
    print(f"""
  {'Traditional University Lab':<35} {'Aviation Research OS':<35}
  {'─'*33:<35} {'─'*33:<35}
  {'Researcher':<35} {'Researcher':<35}
  {'   ↓ (weeks)':<35} {'   ↓ (minutes)':<35}
  {'Manual Google Scholar search':<35} {'LiteratureSearchAgent (SCOPUS/WoS)':<35}
  {'   ↓ (days)':<35} {'   ↓ (minutes)':<35}
  {'Read 40+ papers manually':<35} {'SynthesisAgent (themes + gaps)':<35}
  {'   ↓ (weeks)':<35} {'   ↓ (minutes)':<35}
  {'Brainstorm hypothesis alone':<35} {'GapBrainstormAgent (ranked gaps)':<35}
  {'   ↓ (months)':<35} {'   ↓ (minutes)':<35}
  {'Design methodology by trial':<35} {'ExperimentDesignAgent (blueprint)':<35}
  {'   ↓ (months)':<35} {'   ↓ (minutes)':<35}
  {'Collect data manually':<35} {'QuestionnaireDesignAgent (ready)':<35}
  {'   ↓ (months)':<35} {'   ↓ (minutes)':<35}
  {'SPSS/SmartPLS struggle':<35} {'CodeExecutionAgent (full code)':<35}
  {'   ↓ (weeks)':<35} {'   ↓ (minutes)':<35}
  {'Interpret stats alone':<35} {'AnalysisAgent (full interpretation)':<35}
  {'   ↓ (months)':<35} {'   ↓ (minutes)':<35}
  {'Write paper from scratch':<35} {'PaperWritingAgent (full draft)':<35}
  {'   ↓ (weeks)':<35} {'   ↓ (minutes)':<35}
  {'Submit, get rejected, restart':<35} {'PublicationAgent (submission pkg)':<35}
""")

    # ── Orchestra Positioning ─────────────────────────────────
    box("PRODUCT CATEGORY POSITIONING (Orchestra's Vision)")
    print("""
  Category              Example              Aviation Research OS
  ──────────────────────────────────────────────────────────────
  AI Chat               ChatGPT              ✗ Too generic
  Coding Agent          Claude/Copilot       ✗ Code-centric only
  Research Platform     Elicit, Consensus    ✗ Literature only
  Research OS           Orchestra Research   ✓ Full lifecycle
                        └─ Aviation fork
                           └─ This platform

  Key differentiator: covers the ENTIRE research process
  in ONE session with persistent memory across ALL phases.
""")

    # ── Agent Roster ──────────────────────────────────────────
    box("11 SPECIALIZED RESEARCH AGENTS")
    agents = [
        ("DISCOVERY",   "literature_search",    "Boolean search, PRISMA, 25+ papers"),
        ("DISCOVERY",   "synthesis",            "Thematic map, gaps, framework recommendation"),
        ("IDEATION",    "gap_brainstorm",        "5 gap opportunities, H1–H8, conceptual model"),
        ("DESIGN",      "experiment_design",     "Research paradigm, sampling, power analysis"),
        ("DESIGN",      "questionnaire_design",  "NASA-TLX, SHELL, CRM validated instruments"),
        ("EXECUTION",   "code_execution",        "Python: EFA/CFA/SEM/regression full pipeline"),
        ("ANALYSIS",    "analysis",              "Fit indices, path coefficients, results tables"),
        ("WRITING",     "paper_writing",         "Abstract, intro, discussion — journal-ready"),
        ("WRITING",     "apa_reference",         "APA 7th + ICAO/FAA/EASA document formats"),
        ("PUBLICATION", "publication",           "Cover letter, reviewer response, submission pkg"),
        ("PUBLICATION", "thesis_reviewer",       "Chapter review, viva questions, viva prep"),
    ]
    for phase, name, desc in agents:
        print(f"  [{phase:<11}] {name:<25} {desc}")

    # ── Sample Research Quest ─────────────────────────────────
    box("SAMPLE RESEARCH QUEST — Step-by-step")
    print("""
  RQ: "How does safety culture influence incident reporting
       behavior among commercial pilots in Thailand?"

  ❶ DISCOVERY ─────────────────────────────────────────────
    literature_search → 47 papers from SCOPUS/WoS/ICAO
      Search: TITLE-ABS-KEY("safety culture" AND "incident
              reporting" AND aviation AND "reporting behavior")
    synthesis →
      Dominant theory: Safety Management System (SMS) + HRO
      Key gap: Thai/ASEAN developing-country context missing
      Contradiction: Reason (1997) vs. Pidgeon (1998) on
                     "blame culture" as barrier to reporting

  ❷ IDEATION ──────────────────────────────────────────────
    gap_brainstorm → Selected Gap #2 (novelty score: 8.5/10)
      Conceptual model:
        [Safety Culture] → H1 → [Psychological Safety]
             │                        │
             H2                       H3 (mediator)
             ↓                        ↓
        [Just Culture]  ──H4──→  [Reporting Intention]
                                      │
                                 H5 (moderated by)
                                 [Power Distance — Hofstede]

  ❸ DESIGN ────────────────────────────────────────────────
    experiment_design →
      Cross-sectional survey, stratified sampling
      Thai ATPL holders (N=220, power = 0.80, f²=0.15)
      G*Power: 10 paths × 10 = min n=100; n=220 provides buffer
    questionnaire_design →
      Section A: Safety Culture (8 items, Neal & Griffin 2006)
      Section B: Psychological Safety (7 items, Edmondson 1999)
      Section C: Just Culture (6 items, Dekker 2007, adapted)
      Section D: Reporting Intention (5 items, new scale)
      Section E: Demographics (license, hours, airline, fleet)
      Total: 31 items + 8 demographics, ~12 min to complete
      Back-translation: EN→TH (Translator A) → EN (Translator B)

  ❹ EXECUTION ─────────────────────────────────────────────
    code_execution →
      data_pipeline.py generated (pandas + semopy):
      • 220 responses loaded, 8 outliers removed
      • Cronbach's α: 0.87/0.84/0.81/0.82 (all > 0.70 ✓)
      • Harman's single factor: 28.4% < 50% (CMB low ✓)

  ❺ ANALYSIS ──────────────────────────────────────────────
    analysis →
      CFA fit: χ²/df=2.41, RMSEA=0.069, CFI=0.952 ✓
      AVE: 0.52–0.61 (all > 0.50 ✓)
      HTMT: max 0.71 (all < 0.85 ✓)
      Paths: H1 β=0.42***, H2 β=0.38***, H3 β=0.51***
             H4 β=0.44***, H5 n.s. (Power Distance no effect)
      Mediation: Psych. Safety mediates 61% of Safety Culture→Reporting

  ❻ WRITING ───────────────────────────────────────────────
    paper_writing → Full draft for Safety Science journal
      Title: "Safety Culture, Psychological Safety, and
               Incident Reporting in Thai Commercial Aviation:
               A Structural Equation Modeling Approach"
      Abstract: 247 words (structured, highlights included)
    apa_reference → 38 references formatted APA 7th
      ICAO Doc 9859 (2018) Safety Management Manual formatted ✓

  ❼ PUBLICATION ───────────────────────────────────────────
    publication →
      Target #1: Safety Science (IF 5.76) — 8/10 fit score
      Target #2: Accident Analysis & Prevention — backup
      Cover letter, suggested reviewers, submission checklist
      Expected decision: 12 weeks
""")

    print("=" * W)
    print("  Set ANTHROPIC_API_KEY and run: python main.py chat")
    print("=" * W)


# ─────────────────────────────────────────────────────────────
#  LIVE MODE
# ─────────────────────────────────────────────────────────────

def run_interactive():
    from aviation_research_platform import AviationResearchOS
    print("\n🛫 Aviation Research OS — Interactive Mode")
    print("─" * 55)
    rq = input("Research Question: ").strip()
    domain = input("Domain (e.g. Aviation Safety): ").strip() or "Aviation Research"
    platform = AviationResearchOS.new_session(rq, domain)
    print(f"\nSession: {platform.session.session_id}")
    print("Type 'status' for session status, 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            platform.session.save()
            print(f"Session saved: {platform.session.session_id}")
            break
        if user_input.lower() == "status":
            print(platform.status())
            continue

        response = platform.chat(user_input)
        print(f"\nResearch OS:\n{response}\n")


def run_pipeline_demo():
    from aviation_research_platform import AviationResearchOS, ResearchPhase

    platform = AviationResearchOS.new_session(
        research_question=(
            "How does safety culture influence incident reporting behavior "
            "among commercial airline pilots in Thailand?"
        ),
        domain="Aviation Safety & Human Factors",
    )
    print(f"Session: {platform.session.session_id}")

    for phase in [ResearchPhase.DISCOVERY, ResearchPhase.IDEATION, ResearchPhase.DESIGN]:
        print(f"\n── Phase: {phase.value.upper()} ──")
        results = platform.run_phase(phase)
        for agent, result in results.items():
            print(f"[{agent}]\n{result[:600]}...\n")

    platform.session.save()
    print(f"\nSession saved: {platform.session.session_id}")
    print("Resume with: python main.py status " + platform.session.session_id)


def show_status(session_id: str):
    from aviation_research_platform.core.session import ResearchSession
    from aviation_research_platform import AviationResearchOS
    try:
        platform = AviationResearchOS.resume_session(session_id)
        print(platform.status())
    except FileNotFoundError:
        print(f"Session not found: {session_id}")


# ─────────────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]
    has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))

    if not args or args[0] == "demo":
        print_demo()
        if not has_key:
            sys.exit(0)

    elif args[0] == "chat" and has_key:
        run_interactive()

    elif args[0] == "pipeline" and has_key:
        run_pipeline_demo()

    elif args[0] == "status" and len(args) > 1:
        show_status(args[1])

    else:
        if not has_key:
            print("Set ANTHROPIC_API_KEY to enable live mode.")
            print_demo()
        else:
            print("Usage: python main.py [demo|chat|pipeline|status <id>]")
