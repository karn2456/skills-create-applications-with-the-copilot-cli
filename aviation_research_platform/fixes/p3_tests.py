"""
P3-001: Test Suite
==================
Install: pip install pytest pytest-asyncio

Run: pytest aviation_research_platform/fixes/p3_tests.py -v
"""
from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from aviation_research_platform.core.session import (
    ResearchSession, ResearchPhase, PHASE_ORDER
)
from aviation_research_platform.core.research_graph import ResearchGraph
from aviation_research_platform.core.message_bus import MessageBus, AgentMessage
from aviation_research_platform.core.memory import ResearchMemory


# ─────────────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def session(tmp_path):
    s = ResearchSession.new("How does safety culture affect reporting?", "Aviation Safety")
    # redirect persistence to temp dir
    s._store_dir = str(tmp_path)
    return s


@pytest.fixture
def graph():
    return ResearchGraph()


@pytest.fixture
def bus():
    return MessageBus()


@pytest.fixture
def mock_anthropic_client():
    """Mock anthropic.Anthropic that returns a canned response."""
    mock_response = MagicMock()
    mock_response.stop_reason = "end_turn"
    mock_response.usage.input_tokens = 100
    mock_response.usage.output_tokens = 200

    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "Mock agent response for testing."
    mock_response.content = [text_block]

    client = MagicMock()
    client.messages.create.return_value = mock_response
    return client


# ─────────────────────────────────────────────────────────────
# SESSION TESTS
# ─────────────────────────────────────────────────────────────

class TestResearchSession:

    def test_new_session_has_discovery_phase(self, session):
        assert session.current_phase == ResearchPhase.DISCOVERY

    def test_session_has_unique_id(self):
        s1 = ResearchSession.new("RQ1", "Domain")
        s2 = ResearchSession.new("RQ2", "Domain")
        assert s1.session_id != s2.session_id

    def test_advance_phase_increments(self, session):
        assert session.current_phase == ResearchPhase.DISCOVERY
        next_phase = session.advance_phase()
        assert next_phase == ResearchPhase.IDEATION
        assert session.current_phase == ResearchPhase.IDEATION

    def test_advance_phase_stops_at_publication(self, session):
        for _ in PHASE_ORDER:
            session.advance_phase()
        assert session.current_phase == ResearchPhase.PUBLICATION

    def test_add_artifact_stored(self, session):
        artifact = session.add_artifact(
            phase=ResearchPhase.DISCOVERY,
            agent="literature_search",
            artifact_type="literature_catalog",
            title="Safety Culture Papers",
            content="Found 25 papers.",
        )
        assert len(session.artifacts) == 1
        assert artifact.title == "Safety Culture Papers"
        assert artifact.agent == "literature_search"

    def test_get_artifacts_for_phase(self, session):
        session.add_artifact(ResearchPhase.DISCOVERY, "a1", "type1", "T1", "C1")
        session.add_artifact(ResearchPhase.IDEATION,  "a2", "type2", "T2", "C2")
        session.add_artifact(ResearchPhase.DISCOVERY, "a3", "type3", "T3", "C3")

        discovery = session.get_artifacts_for_phase(ResearchPhase.DISCOVERY)
        assert len(discovery) == 2

    def test_add_dead_end(self, session):
        session.add_dead_end("HFACS not applicable here", "synthesis")
        assert len(session.dead_ends) == 1
        assert session.dead_ends[0]["description"] == "HFACS not applicable here"

    def test_context_summary_includes_rq(self, session):
        summary = session.context_summary()
        assert session.research_question in summary

    def test_progress_bar_shows_current_phase(self, session):
        bar = session.progress_bar()
        assert "▶ discovery" in bar
        assert "  ideation" in bar

    def test_session_save_load(self, session, tmp_path):
        session.add_artifact(ResearchPhase.DISCOVERY, "agent", "type", "title", "content")
        session.save(str(tmp_path))

        loaded = ResearchSession.load(session.session_id, str(tmp_path))
        assert loaded.session_id == session.session_id
        assert loaded.research_question == session.research_question
        assert len(loaded.artifacts) == 1


# ─────────────────────────────────────────────────────────────
# RESEARCH GRAPH TESTS
# ─────────────────────────────────────────────────────────────

class TestResearchGraph:

    def test_add_node(self, graph):
        node = graph.add_node("p1", "paper", "Reason 1990",
                               "Swiss cheese model of accidents")
        assert node.node_id == "p1"
        assert node.kind == "paper"

    def test_add_edge(self, graph):
        graph.add_node("p1", "paper", "Reason 1990", "Swiss cheese")
        graph.add_node("h1", "hypothesis", "H1", "Safety culture → reporting")
        graph.add_edge("p1", "h1", "informs")
        assert len(graph._edges) == 1

    def test_neighbors(self, graph):
        graph.add_node("p1", "paper", "P1", "Abstract 1")
        graph.add_node("h1", "hypothesis", "H1", "Hypothesis 1")
        graph.add_node("h2", "hypothesis", "H2", "Hypothesis 2")
        graph.add_edge("p1", "h1", "informs")
        graph.add_edge("p1", "h2", "informs")
        neighbors = graph.neighbors("p1")
        assert len(neighbors) == 2

    def test_find_gaps(self, graph):
        graph.add_node("g1", "gap", "Thai context missing", "No SE Asian studies")
        graph.add_node("p1", "paper", "Some paper", "Abstract")
        gaps = graph.find_gaps()
        assert len(gaps) == 1

    def test_find_contradictions(self, graph):
        graph.add_node("p1", "paper", "P1", "A1")
        graph.add_node("p2", "paper", "P2", "A2")
        graph.add_edge("p1", "p2", "contradicts")
        contras = graph.find_contradictions()
        assert len(contras) == 1

    def test_path_exists(self, graph):
        graph.add_node("a", "paper", "A", "")
        graph.add_node("b", "hypothesis", "B", "")
        graph.add_node("c", "finding", "C", "")
        graph.add_edge("a", "b", "informs")
        graph.add_edge("b", "c", "derived_from")
        assert graph.path_exists("a", "c")
        assert not graph.path_exists("c", "a")  # directed


# ─────────────────────────────────────────────────────────────
# MESSAGE BUS TESTS
# ─────────────────────────────────────────────────────────────

class TestMessageBus:

    def test_publish_consume(self, bus):
        msg = AgentMessage(
            sender="literature_search",
            receiver="orchestrator",
            message_type="result",
            payload={"result": "Found 25 papers"},
        )
        bus.publish(msg)
        consumed = bus.consume("orchestrator")
        assert len(consumed) == 1
        assert consumed[0].sender == "literature_search"

    def test_consume_empty_returns_empty_list(self, bus):
        assert bus.consume("nonexistent_agent") == []

    def test_subscribe_handler_called(self, bus):
        received = []
        bus.subscribe("orchestrator", lambda m: received.append(m))
        msg = AgentMessage("sender", "orchestrator", "result", {})
        bus.publish(msg)
        assert len(received) == 1


# ─────────────────────────────────────────────────────────────
# AGENT SMOKE TESTS (mock LLM)
# ─────────────────────────────────────────────────────────────

class TestAgentSmoke:
    """Quick smoke tests: agents init correctly and run() returns a string."""

    def _make_session(self):
        return ResearchSession.new("Test RQ", "Aviation Safety")

    def test_literature_search_agent_init(self, mock_anthropic_client):
        from aviation_research_platform.agents.literature_search_agent import LiteratureSearchAgent
        session = self._make_session()
        bus = MessageBus()
        agent = LiteratureSearchAgent(session, bus, mock_anthropic_client)
        assert agent.name == "literature_search"
        assert "Aviation Literature Search" in agent.system_prompt

    def test_gap_brainstorm_agent_run(self, mock_anthropic_client):
        from aviation_research_platform.agents.gap_brainstorm_agent import GapBrainstormAgent
        session = self._make_session()
        bus = MessageBus()
        agent = GapBrainstormAgent(session, bus, mock_anthropic_client)
        result = agent.run("Brainstorm gaps in aviation safety culture research")
        assert isinstance(result, str)
        assert len(result) > 0
        # Artifact should be stored in session
        assert len(session.artifacts) == 1

    def test_analysis_agent_run_stores_artifact(self, mock_anthropic_client):
        from aviation_research_platform.agents.analysis_agent import AnalysisAgent
        session = self._make_session()
        bus = MessageBus()
        agent = AnalysisAgent(session, bus, mock_anthropic_client)
        agent.run("Interpret SEM results", artifact_type="analysis_results")
        assert session.artifacts[0].artifact_type == "analysis_results"

    def test_orchestrator_init(self, mock_anthropic_client):
        from aviation_research_platform.core.orchestrator import AviationResearchOS
        session = self._make_session()
        with patch("anthropic.Anthropic", return_value=mock_anthropic_client):
            os_platform = AviationResearchOS(session, api_key="test-key")
        assert len(os_platform.agents) == 11
