"""
Developer Handoff: Aviation Research OS
========================================
ไฟล์นี้ระบุทุก gap ระหว่าง prototype กับ production
พร้อม code fix และ priority สำหรับ developer ที่รับงานต่อ

Priority:
  P0 = โค้ดพังถ้าไม่แก้ (ต้องทำก่อน)
  P1 = ใช้งานได้แต่ไม่ถูกต้อง (ควรทำใน sprint แรก)
  P2 = ยังไม่มีแต่ผู้ใช้ต้องการ (sprint 2-3)
  P3 = nice-to-have (backlog)
"""

GAP_REGISTRY = [

    # ─────────────────────────────────────────────────────────────────
    # P0: TOOL USE LOOP BROKEN
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "P0-001",
        "title": "Tool use loop ไม่ทำงาน",
        "file": "aviation_research_platform/core/base_agent.py",
        "problem": """
        _call_llm() ดึงเฉพาะ text blocks จาก response.content
        แต่เมื่อ LLM เรียก tool ผลลัพธ์จะเป็น tool_use block ไม่ใช่ text block
        → agent ไม่เคยได้ผลลัพธ์จาก tool จริงๆ เลย
        """,
        "current_code": """
        # base_agent.py line 79-81 — BROKEN
        return "\\n".join(
            block.text for block in response.content if hasattr(block, "text")
        )
        """,
        "fix": "ดู fixes/p0_tool_use_loop.py",
    },

    # ─────────────────────────────────────────────────────────────────
    # P0: AGENTS ใช้ CONSTRUCTOR ARGUMENT ต่างกัน
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "P0-002",
        "title": "QuestionnaireDesignAgent และ APAReferenceAgent ใช้ API เก่า",
        "file": "aviation_research_platform/core/orchestrator.py",
        "problem": """
        QDesignAgent และ APAReferenceAgent รับ (memory, bus, client)
        แต่ agents ใหม่ทั้งหมดรับ (session, bus, client)
        → orchestrator ส่ง args ผิดทำให้ crash ตอน init
        """,
        "fix": "ดู fixes/p0_agent_api_alignment.py",
    },

    # ─────────────────────────────────────────────────────────────────
    # P1: ไม่มี REAL DATABASE SEARCH
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "P1-001",
        "title": "LiteratureSearchAgent ไม่ได้ค้นหาจริง — simulate เท่านั้น",
        "file": "aviation_research_platform/agents/literature_search_agent.py",
        "problem": """
        agent บอก LLM ให้ 'simulate' ผลการค้นหา
        ผลลัพธ์ = LLM hallucinate รายชื่อ paper ที่ไม่มีจริง
        """,
        "fix": "ดู fixes/p1_real_search_apis.py — Semantic Scholar + CrossRef + arXiv (free)",
    },

    # ─────────────────────────────────────────────────────────────────
    # P1: CODE EXECUTION ปิดอยู่
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "P1-002",
        "title": "CodeExecutionAgent ไม่ execute จริง (disabled by default)",
        "file": "aviation_research_platform/agents/code_execution_agent.py",
        "problem": """
        enable_execution=False ทำให้ทุก exec call return placeholder text
        subprocess sandbox ยังไม่มี resource limits / network isolation
        """,
        "fix": "ดู fixes/p1_sandbox_execution.py — Docker sandbox หรือ E2B cloud sandbox",
    },

    # ─────────────────────────────────────────────────────────────────
    # P1: ไม่มี STREAMING
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "P1-003",
        "title": "ไม่มี streaming — รอนาน, UX แย่",
        "file": "aviation_research_platform/core/base_agent.py",
        "problem": """
        ทุก LLM call รอจนจบก่อน return
        agent ที่ generate 4096 tokens = รอ 30-60 วินาทีโดยไม่มี feedback
        """,
        "fix": "ดู fixes/p1_streaming.py — anthropic streaming + callback",
    },

    # ─────────────────────────────────────────────────────────────────
    # P1: ไม่มี RETRY / RATE LIMITING
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "P1-004",
        "title": "ไม่มี error handling สำหรับ API failures",
        "file": "aviation_research_platform/core/base_agent.py",
        "problem": """
        ถ้า Anthropic API ตอบ 529 (overloaded) หรือ 429 (rate limit)
        โค้ดจะ crash ทันที ไม่มี retry
        """,
        "fix": "ดู fixes/p1_retry.py — tenacity exponential backoff",
    },

    # ─────────────────────────────────────────────────────────────────
    # P2: ไม่มี WEB UI
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "P2-001",
        "title": "CLI เท่านั้น — ไม่มี Web Interface",
        "file": "main.py",
        "problem": "นักวิจัยต้องการ web UI ไม่ใช่ terminal",
        "fix": "ดู fixes/p2_fastapi_backend.py — FastAPI + WebSocket สำหรับ streaming",
    },

    # ─────────────────────────────────────────────────────────────────
    # P2: COST ไม่ถูกควบคุม
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "P2-002",
        "title": "ทุก agent ใช้ claude-opus-4-8 — แพงเกินไปสำหรับทุก call",
        "file": "aviation_research_platform/core/base_agent.py",
        "problem": """
        routing call (simple classification) ก็ใช้ opus-4-8 เหมือนกัน
        orchestrator route 1 ครั้ง + agent run 1 ครั้ง + synthesize = 3x opus call
        ประมาณ $0.15-0.60 ต่อ 1 interaction
        """,
        "fix": "ดู fixes/p2_model_routing.py — haiku สำหรับ routing, opus สำหรับ research",
    },

    # ─────────────────────────────────────────────────────────────────
    # P2: ไม่มี MULTI-USER
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "P2-003",
        "title": "Session เก็บเป็น JSON file — ไม่รองรับ multi-user",
        "file": "aviation_research_platform/core/session.py",
        "problem": "ใช้ไฟล์ local filesystem — ไม่ scale, ไม่มี auth, ไม่มี isolation",
        "fix": "ดู fixes/p2_database_session.py — SQLite (dev) หรือ PostgreSQL (prod)",
    },

    # ─────────────────────────────────────────────────────────────────
    # P3: ไม่มี TESTS
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "P3-001",
        "title": "ไม่มี test suite",
        "fix": "ดู fixes/p3_tests.py — pytest + mock Anthropic client",
    },
]
