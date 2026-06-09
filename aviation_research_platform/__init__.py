"""
Aviation Research OS — AI-native research platform for aviation researchers.
Covers the full lifecycle: Discovery → Ideation → Design → Execution → Analysis → Writing → Publication.

Inspired by Orchestra Research's Research IDE architecture.
Implements: multi-agent orchestration + long-horizon memory + human-in-the-loop.
"""
from .core.orchestrator import AviationResearchOS
from .core.session import ResearchSession, ResearchPhase

__version__ = "1.0.0"
__all__ = ["AviationResearchOS", "ResearchSession", "ResearchPhase"]
