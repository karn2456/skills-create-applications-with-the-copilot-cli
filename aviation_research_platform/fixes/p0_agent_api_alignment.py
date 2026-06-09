"""
P0-002 FIX: Agent Constructor API Alignment
============================================
ปัญหา: agents 2 ตัวใช้ constructor signature เก่า → crash ตอน init

แก้ใน 2 ไฟล์:
  questionnaire_design_agent.py  line ~12: __init__(self, memory, bus, client)
  apa_reference_agent.py         line ~12: __init__(self, memory, bus, client)

  แก้เป็น: __init__(self, session, bus, client)
  และเปลี่ยน self.memory → self.session ทุกที่ใน file

แก้ใน orchestrator.py:
  เปลี่ยน 2 บรรทัดนี้ใน _init_agents()
"""

# ── OLD CODE (orchestrator.py _init_agents) ──────────────────────────────
OLD_INIT_AGENTS = """
    "questionnaire_design": QuestionnaireDesignAgent(
                                self.memory, self.bus, self.client),
    ...
    "apa_reference":        APAReferenceAgent(self.memory, self.bus, self.client),
"""

# ── NEW CODE ──────────────────────────────────────────────────────────────
NEW_INIT_AGENTS = """
    "questionnaire_design": QuestionnaireDesignAgent(*args),
    ...
    "apa_reference":        APAReferenceAgent(*args),
"""

# ── HOW TO FIX questionnaire_design_agent.py ────────────────────────────
QUESTIONNAIRE_FIX = """
# OLD:
class QuestionnaireDesignAgent(BaseResearchAgent):
    def __init__(self, memory, bus, client):
        super().__init__(self.NAME, memory, bus, client)
        self.memory = memory

# NEW:
class QuestionnaireDesignAgent(BaseResearchAgent):
    NAME = "questionnaire_design"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.DESIGN, session, bus, client)
"""

# ── HOW TO FIX apa_reference_agent.py ───────────────────────────────────
APA_FIX = """
# OLD:
class APAReferenceAgent(BaseResearchAgent):
    def __init__(self, memory, bus, client):
        super().__init__(self.NAME, memory, bus, client)

# NEW:
class APAReferenceAgent(BaseResearchAgent):
    NAME = "apa_reference"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.WRITING, session, bus, client)
"""

# ── HOW TO FIX thesis_reviewer_agent.py ─────────────────────────────────
THESIS_FIX = """
# OLD:
class ThesisReviewerAgent(BaseResearchAgent):
    def __init__(self, memory, bus, client):
        super().__init__(self.NAME, memory, bus, client)

# NEW:
class ThesisReviewerAgent(BaseResearchAgent):
    NAME = "thesis_reviewer"

    def __init__(self, session, bus, client):
        super().__init__(self.NAME, ResearchPhase.PUBLICATION, session, bus, client)
"""

print("Apply the patches above to fix P0-002.")
print("All agents must use: __init__(self, session, bus, client)")
