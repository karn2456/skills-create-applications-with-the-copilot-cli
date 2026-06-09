"""
Aviation Research Orchestrator — the Research OS brain.

Implements Orchestra's core pattern:
  - Researcher proposes direction & supervises
  - Orchestrator routes to specialized agents
  - Agents execute each phase end-to-end
  - Long-horizon memory (ResearchSession) persists everything
  - Human gates at phase transitions

Architecture mirrors:
  Orchestra Research Companion  ↔  Duo Chat (GitLab)
  Three-Layer (Cognitive/Eng/Infra)  ↔  Task-Router + Sub-agents
  Total Recall (months)  ↔  Session + Repo context
"""
from __future__ import annotations

import os
import re
import json
from typing import Any

import anthropic

from .session import ResearchSession, ResearchPhase, PHASE_ORDER
from .message_bus import MessageBus
from .memory import ResearchMemory
from .research_graph import ResearchGraph

from ..agents.literature_search_agent import LiteratureSearchAgent
from ..agents.synthesis_agent import SynthesisAgent
from ..agents.gap_brainstorm_agent import GapBrainstormAgent
from ..agents.experiment_design_agent import ExperimentDesignAgent
from ..agents.code_execution_agent import CodeExecutionAgent
from ..agents.analysis_agent import AnalysisAgent
from ..agents.paper_writing_agent import PaperWritingAgent
from ..agents.publication_agent import PublicationAgent

# Keep specialized domain agents from original platform
from ..agents.questionnaire_design_agent import QuestionnaireDesignAgent
from ..agents.apa_reference_agent import APAReferenceAgent
from ..agents.thesis_reviewer_agent import ThesisReviewerAgent


ORCHESTRATOR_SYSTEM = """You are the Aviation Research OS — an orchestrator coordinating a
team of specialized AI research agents for aviation researchers.

Your agents (by research phase):
DISCOVERY  : literature_search, synthesis
IDEATION   : gap_brainstorm
DESIGN     : experiment_design, questionnaire_design
EXECUTION  : code_execution
ANALYSIS   : analysis
WRITING    : paper_writing, apa_reference
PUBLICATION: publication, thesis_reviewer

Routing rules:
- "find papers / search literature / what papers" → literature_search
- "synthesize / map / what do we know / themes" → synthesis
- "gap / hypothesis / what to study / conceptual model" → gap_brainstorm
- "methodology / design / sample / instrument" → experiment_design
- "questionnaire / survey / scale" → questionnaire_design
- "code / analysis code / python / R / run" → code_execution
- "results / SEM output / fit indices / interpret" → analysis
- "write / draft / abstract / introduction / section" → paper_writing
- "reference / citation / APA" → apa_reference
- "submit / journal / cover letter / reviewer" → publication
- "review thesis / chapter / viva / defense" → thesis_reviewer

Multi-phase tasks: route to multiple agents in sequence.
Always respond in the researcher's language (Thai or English)."""


class AviationResearchOS:
    """
    The Aviation Research Operating System.

    Usage:
        os = AviationResearchOS.new_session(
            research_question="How does...",
            domain="Aviation Safety"
        )
        response = os.chat("I need to find papers on safety culture in airlines")
        response = os.run_phase(ResearchPhase.DISCOVERY)
    """

    def __init__(self, session: ResearchSession, api_key: str | None = None):
        self.session = session
        self.client = anthropic.Anthropic(api_key=api_key or os.environ["ANTHROPIC_API_KEY"])
        self.bus = MessageBus()
        self.memory = ResearchMemory(session.session_id)
        self.graph = ResearchGraph()

        self.agents: dict[str, Any] = self._init_agents()
        self._conversation: list[dict] = []

    @classmethod
    def new_session(cls, research_question: str, domain: str,
                    api_key: str | None = None) -> "AviationResearchOS":
        session = ResearchSession.new(research_question, domain)
        return cls(session, api_key)

    @classmethod
    def resume_session(cls, session_id: str, api_key: str | None = None) -> "AviationResearchOS":
        session = ResearchSession.load(session_id)
        return cls(session, api_key)

    def _init_agents(self) -> dict[str, Any]:
        args = (self.session, self.bus, self.client)
        return {
            # Discovery phase
            "literature_search":    LiteratureSearchAgent(*args),
            "synthesis":            SynthesisAgent(*args),
            # Ideation phase
            "gap_brainstorm":       GapBrainstormAgent(*args),
            # Design phase
            "experiment_design":    ExperimentDesignAgent(*args),
            "questionnaire_design": QuestionnaireDesignAgent(*args),
            # Execution phase
            "code_execution":       CodeExecutionAgent(*args),
            # Analysis phase
            "analysis":             AnalysisAgent(*args),
            # Writing phase
            "paper_writing":        PaperWritingAgent(*args),
            "apa_reference":        APAReferenceAgent(*args),
            # Publication phase
            "publication":          PublicationAgent(*args),
            "thesis_reviewer":      ThesisReviewerAgent(*args),
        }

    # ── Public API ────────────────────────────────────────────────────────────

    def chat(self, user_input: str) -> str:
        """
        Human-in-the-loop entry: researcher speaks, orchestrator routes, agents execute.
        This is the core interaction model of Orchestra's Research IDE.
        """
        ctx = self.session.context_summary()
        self._conversation.append({
            "role": "user",
            "content": f"[Session context]\n{ctx}\n\n[Researcher]: {user_input}",
        })

        # Step 1: Orchestrator decides routing
        routing = self._route(user_input)

        # Step 2: Execute routed agents
        results = self._execute_routing(routing, user_input)

        # Step 3: Synthesize if multiple agents ran
        final = self._synthesize(user_input, results)

        self._conversation.append({"role": "assistant", "content": final})
        self.session.save()
        return final

    def run_phase(self, phase: ResearchPhase) -> dict[str, str]:
        """Run all agents for a specific research phase. Returns dict of agent → result."""
        phase_agents = {
            ResearchPhase.DISCOVERY:   ["literature_search", "synthesis"],
            ResearchPhase.IDEATION:    ["gap_brainstorm"],
            ResearchPhase.DESIGN:      ["experiment_design", "questionnaire_design"],
            ResearchPhase.EXECUTION:   ["code_execution"],
            ResearchPhase.ANALYSIS:    ["analysis"],
            ResearchPhase.WRITING:     ["paper_writing", "apa_reference"],
            ResearchPhase.PUBLICATION: ["publication"],
        }

        rq = self.session.research_question
        results: dict[str, str] = {}

        for agent_name in phase_agents.get(phase, []):
            agent = self.agents[agent_name]
            print(f"  [{phase.value}] Running {agent_name}...")
            result = agent.run(
                task=f"Advance the research for: {rq}\nPhase: {phase.value}",
                artifact_type=f"{phase.value}_output",
            )
            results[agent_name] = result

        self.session.current_phase = phase
        self.session.save()
        return results

    def run_full_pipeline(self) -> list[dict[str, str]]:
        """
        Run the complete research lifecycle end-to-end.
        Mirrors Orchestra's "end-to-end, one place" workflow.
        Human gates: pauses before DESIGN, WRITING, PUBLICATION for researcher input.
        """
        all_results = []
        human_gate_phases = {ResearchPhase.DESIGN, ResearchPhase.WRITING, ResearchPhase.PUBLICATION}

        for phase in PHASE_ORDER:
            print(f"\n{'='*55}")
            print(f" Phase: {phase.value.upper()}")
            print(f"{'='*55}")

            if phase in human_gate_phases:
                print(f"\n⏸  Human Gate — Phase: {phase.value}")
                print(f"   Review artifacts from previous phase before continuing.")
                print(f"   Progress: {self.session.progress_bar()}")
                print(f"   Type 'continue' to proceed or 'skip' to advance...\n")

            results = self.run_phase(phase)
            all_results.append({phase.value: results})

        return all_results

    def status(self) -> str:
        """Return current session status and progress."""
        lines = [
            f"Session ID : {self.session.session_id}",
            f"RQ         : {self.session.research_question}",
            f"Domain     : {self.session.domain}",
            f"Progress   : {self.session.progress_bar()}",
            f"Artifacts  : {len(self.session.artifacts)}",
            f"Hypotheses : {len(self.session.hypotheses)}",
            f"Dead ends  : {len(self.session.dead_ends)}",
            f"Graph      : {len(self.graph._nodes)} nodes",
            "",
            "Artifacts by phase:",
        ]
        for phase in PHASE_ORDER:
            artifacts = self.session.get_artifacts_for_phase(phase)
            if artifacts:
                lines.append(f"  [{phase.value}] {len(artifacts)} artifacts")
                for a in artifacts[:3]:
                    lines.append(f"    • {a.artifact_type}: {a.title[:60]}")
        return "\n".join(lines)

    # ── Routing internals ─────────────────────────────────────────────────────

    def _route(self, user_input: str) -> list[dict]:
        """Ask orchestrator LLM to route the request."""
        resp = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=512,
            system=ORCHESTRATOR_SYSTEM + "\n\nRespond ONLY with JSON: {\"routes\": [{\"agent\": \"...\", \"task\": \"...\"}]}",
            messages=[{"role": "user", "content": user_input}],
        )
        text = resp.content[0].text
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group()).get("routes", [])
            except json.JSONDecodeError:
                pass
        # Fallback: direct answer from orchestrator
        return [{"agent": "__direct__", "task": user_input, "_direct_answer": text}]

    def _execute_routing(self, routes: list[dict], original: str) -> list[dict]:
        results = []
        for route in routes:
            agent_name = route.get("agent", "")
            task = route.get("task", original)

            if agent_name == "__direct__":
                results.append({"agent": "orchestrator", "result": route.get("_direct_answer", "")})
                continue

            if agent_name in self.agents:
                print(f"  → {agent_name}")
                result = self.agents[agent_name].run(task)
                results.append({"agent": agent_name, "result": result})
            else:
                # Unknown agent — answer directly
                fallback = self.client.messages.create(
                    model="claude-opus-4-8",
                    max_tokens=2048,
                    system=ORCHESTRATOR_SYSTEM,
                    messages=[{"role": "user", "content": task}],
                )
                results.append({"agent": "orchestrator", "result": fallback.content[0].text})

        return results

    def _synthesize(self, user_input: str, results: list[dict]) -> str:
        if not results:
            return "No agent produced a result. Please rephrase your request."
        if len(results) == 1:
            return results[0]["result"]

        combined = "\n\n".join(
            f"=== {r['agent']} ===\n{r['result']}" for r in results
        )
        resp = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4096,
            system=ORCHESTRATOR_SYSTEM,
            messages=[{
                "role": "user",
                "content": (
                    f"Researcher asked: {user_input}\n\n"
                    f"Multiple agents responded:\n{combined}\n\n"
                    "Synthesize into one coherent, well-organized response. "
                    "Preserve all key content; remove redundancy."
                ),
            }],
        )
        return resp.content[0].text
