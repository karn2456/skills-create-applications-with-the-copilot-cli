"""
Aviation Research Orchestrator — the central intelligence that routes research tasks
to specialized agents, maintains session state, and synthesizes results.

Pattern: mirrors Orchestra's Research Companion + GitLab Duo's Duo Chat orchestrator.
"""
from __future__ import annotations

import os
import uuid
from typing import Any

import anthropic

from .memory import ResearchMemory
from .message_bus import MessageBus
from ..agents.literature_review_agent import LiteratureReviewAgent
from ..agents.questionnaire_design_agent import QuestionnaireDesignAgent
from ..agents.sem_analysis_agent import SEMAnalysisAgent
from ..agents.apa_reference_agent import APAReferenceAgent
from ..agents.thesis_reviewer_agent import ThesisReviewerAgent


ORCHESTRATOR_SYSTEM = """You are the Aviation Research Orchestrator — the central intelligence
of the Aviation Research Agent Platform (ARA). You coordinate a team of specialized AI research agents.

Your agents:
1. literature_review_agent — surveys aviation papers, maps knowledge frontiers, identifies gaps
2. questionnaire_design_agent — designs validated survey instruments for aviation research
3. sem_analysis_agent — guides SEM/CFA/PLS-SEM statistical analysis
4. apa_reference_agent — formats and validates APA 7th edition references
5. thesis_reviewer_agent — reviews thesis chapters and prepares viva defense

Your role:
- Understand the researcher's intent and decompose it into agent tasks
- Route tasks to the correct specialized agent(s)
- Synthesize results from multiple agents into a coherent research workflow
- Maintain long-horizon research context (what has been done, what's next)
- Flag when tasks require human decision (Human-in-the-Loop gates)

Decision Protocol:
- If intent is literature survey → route to literature_review_agent
- If intent is survey/questionnaire → route to questionnaire_design_agent
- If intent is statistical analysis → route to sem_analysis_agent
- If intent is references/citations → route to apa_reference_agent
- If intent is thesis review/defense → route to thesis_reviewer_agent
- If intent spans multiple areas → coordinate multi-agent pipeline

Always respond in the same language the researcher uses.
For Thai researchers, respond in Thai. For English, respond in English."""


class AviationResearchOrchestrator:
    """
    Central orchestrator for the Aviation Research Agent Platform.

    Architecture mirrors:
    - Orchestra ARA: Research Companion with long-horizon memory
    - GitLab Duo: Duo Chat with specialized sub-agents
    """

    def __init__(self, api_key: str | None = None, session_id: str | None = None):
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.client = anthropic.Anthropic(api_key=api_key or os.environ["ANTHROPIC_API_KEY"])
        self.memory = ResearchMemory(self.session_id)
        self.bus = MessageBus()

        # Initialize specialized agents (the "sub-agents" in agent platform pattern)
        self.agents: dict[str, Any] = {
            "literature_review_agent": LiteratureReviewAgent(self.memory, self.bus, self.client),
            "questionnaire_design_agent": QuestionnaireDesignAgent(self.memory, self.bus, self.client),
            "sem_analysis_agent": SEMAnalysisAgent(self.memory, self.bus, self.client),
            "apa_reference_agent": APAReferenceAgent(self.memory, self.bus, self.client),
            "thesis_reviewer_agent": ThesisReviewerAgent(self.memory, self.bus, self.client),
        }

        self._conversation: list[dict] = []
        print(f"\n🛫 Aviation Research Agent Platform initialized — Session: {self.session_id}")
        print(f"   Agents ready: {', '.join(self.agents.keys())}\n")

    def chat(self, user_input: str) -> str:
        """
        Main entry point: receive researcher input, route to agents, return synthesized result.
        This is the Human-in-the-Loop gate — researcher drives the research direction.
        """
        prior_context = self.memory.get_context_summary()

        # Build orchestrator routing message
        routing_prompt = f"""{prior_context}

Researcher message: {user_input}

Determine:
1. Which agent(s) should handle this request
2. What specific task to send each agent
3. How to synthesize their outputs

Then respond with your routing decision in this JSON format:
{{
  "routing": [
    {{"agent": "agent_name", "task": "specific task description"}}
  ],
  "reasoning": "why this routing"
}}"""

        self._conversation.append({"role": "user", "content": routing_prompt})

        # Orchestrator decides routing
        routing_response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            system=ORCHESTRATOR_SYSTEM,
            messages=self._conversation,
        )

        routing_text = routing_response.content[0].text
        self._conversation.append({"role": "assistant", "content": routing_text})

        # Extract routing decisions and execute agents
        results = self._execute_routing(routing_text, user_input)

        # Synthesize results
        final_response = self._synthesize(user_input, results)
        self.memory.add("orchestrator", "result", final_response, user_input=user_input)

        return final_response

    def _execute_routing(self, routing_text: str, original_input: str) -> list[dict]:
        """Parse routing decision and execute appropriate agents."""
        import json
        import re

        results = []
        json_match = re.search(r'\{.*\}', routing_text, re.DOTALL)

        if json_match:
            try:
                routing = json.loads(json_match.group())
                for route in routing.get("routing", []):
                    agent_name = route.get("agent", "")
                    task = route.get("task", original_input)
                    if agent_name in self.agents:
                        print(f"   → Routing to {agent_name}...")
                        result = self.agents[agent_name].run(task)
                        results.append({"agent": agent_name, "result": result})
            except json.JSONDecodeError:
                pass

        # Fallback: if no routing parsed, use LLM to answer directly
        if not results:
            direct_response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=4096,
                system=ORCHESTRATOR_SYSTEM,
                messages=[{"role": "user", "content": original_input}],
            )
            results.append({
                "agent": "orchestrator_direct",
                "result": direct_response.content[0].text,
            })

        return results

    def _synthesize(self, user_input: str, results: list[dict]) -> str:
        """Synthesize multi-agent results into a coherent response."""
        if len(results) == 1:
            return results[0]["result"]

        combined = "\n\n".join(
            f"=== {r['agent']} ===\n{r['result']}" for r in results
        )

        synth_response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4096,
            system=ORCHESTRATOR_SYSTEM,
            messages=[{
                "role": "user",
                "content": f"""The researcher asked: {user_input}

Multiple agents produced these results:
{combined}

Synthesize these into a single coherent, well-organized response for the researcher.
Preserve all important details but eliminate redundancy."""
            }],
        )
        return synth_response.content[0].text

    def run_full_research_pipeline(
        self,
        research_question: str,
        topic: str,
        constructs: list[str],
        target_population: str,
        sample_size: int,
    ) -> dict[str, str]:
        """
        Execute the full aviation research workflow pipeline.
        Mirrors Orchestra's end-to-end research loop.
        """
        print("\n🔬 Starting Full Aviation Research Pipeline...")
        results = {}

        print("\n[1/4] Literature Review Agent...")
        lit = self.agents["literature_review_agent"]
        results["literature_review"] = lit.review(research_question, topic)

        print("\n[2/4] Questionnaire Design Agent...")
        quest = self.agents["questionnaire_design_agent"]
        results["questionnaire"] = quest.design(research_question, constructs, target_population)

        print("\n[3/4] SEM Analysis Agent...")
        sem = self.agents["sem_analysis_agent"]
        hypotheses = [f"{constructs[i]} → {constructs[i+1]}" for i in range(len(constructs)-1)]
        results["sem_analysis"] = sem.analyze(
            f"Model: {' → '.join(constructs)}",
            hypotheses,
            sample_size,
        )

        print("\n[4/4] APA Reference Agent...")
        apa = self.agents["apa_reference_agent"]
        results["references"] = apa.generate_reference_list(topic)

        print("\n✅ Research pipeline complete.\n")
        return results
