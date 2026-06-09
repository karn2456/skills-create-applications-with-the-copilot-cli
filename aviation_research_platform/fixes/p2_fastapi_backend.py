"""
P2-001 FIX: FastAPI Web Backend with WebSocket streaming
=========================================================
Install: pip install fastapi uvicorn websockets python-multipart

Run: uvicorn aviation_research_platform.fixes.p2_fastapi_backend:app --reload

Endpoints:
  POST /sessions/new        → สร้าง session ใหม่
  POST /sessions/{id}/chat  → ส่ง message (sync response)
  WS   /sessions/{id}/ws    → WebSocket streaming response
  GET  /sessions/{id}/status→ ดู session status
  GET  /sessions            → list sessions ทั้งหมด
"""
from __future__ import annotations

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Thread pool for running sync agent code in async context ──────────────
_executor = ThreadPoolExecutor(max_workers=4)

app = FastAPI(title="Aviation Research OS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory session registry (replace with DB for production) ───────────
_sessions: dict[str, Any] = {}


# ─────────────────────────────────────────────────────────────
# REQUEST / RESPONSE MODELS
# ─────────────────────────────────────────────────────────────

class NewSessionRequest(BaseModel):
    research_question: str
    domain: str = "Aviation Research"
    api_key: str | None = None


class ChatRequest(BaseModel):
    message: str


class SessionStatus(BaseModel):
    session_id: str
    research_question: str
    current_phase: str
    artifact_count: int
    progress: str


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _get_platform(session_id: str):
    """Get or raise 404."""
    platform = _sessions.get(session_id)
    if not platform:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    return platform


async def _run_in_thread(fn, *args):
    """Run sync function in thread pool without blocking event loop."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, fn, *args)


# ─────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────

@app.post("/sessions/new", response_model=dict)
async def new_session(req: NewSessionRequest):
    from aviation_research_platform import AviationResearchOS
    api_key = req.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(400, "ANTHROPIC_API_KEY required")

    platform = await _run_in_thread(
        AviationResearchOS.new_session,
        req.research_question,
        req.domain,
        api_key,
    )
    _sessions[platform.session.session_id] = platform
    return {
        "session_id": platform.session.session_id,
        "message": "Session created successfully",
    }


@app.post("/sessions/{session_id}/chat", response_model=dict)
async def chat(session_id: str, req: ChatRequest):
    platform = _get_platform(session_id)
    response = await _run_in_thread(platform.chat, req.message)
    return {"response": response, "session_id": session_id}


@app.get("/sessions/{session_id}/status", response_model=SessionStatus)
async def get_status(session_id: str):
    platform = _get_platform(session_id)
    s = platform.session
    return SessionStatus(
        session_id=s.session_id,
        research_question=s.research_question,
        current_phase=s.current_phase.value,
        artifact_count=len(s.artifacts),
        progress=s.progress_bar(),
    )


@app.get("/sessions", response_model=list)
async def list_sessions():
    return [
        {
            "session_id": sid,
            "rq": p.session.research_question[:80],
            "phase": p.session.current_phase.value,
        }
        for sid, p in _sessions.items()
    ]


@app.websocket("/sessions/{session_id}/ws")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for streaming responses.

    Client sends: {"message": "find papers on safety culture"}
    Server streams: text chunks, ends with {"done": true, "session_id": "..."}

    JavaScript client example:
        const ws = new WebSocket(`ws://localhost:8000/sessions/${id}/ws`);
        ws.onmessage = (e) => {
            const data = JSON.parse(e.data);
            if (data.chunk) appendToUI(data.chunk);
            if (data.done)  finalizeUI();
        };
        ws.send(JSON.stringify({message: "search for aviation safety papers"}));
    """
    await websocket.accept()
    platform = _sessions.get(session_id)
    if not platform:
        await websocket.send_json({"error": f"Session {session_id} not found"})
        await websocket.close()
        return

    try:
        while True:
            data = await websocket.receive_json()
            user_message = data.get("message", "")
            if not user_message:
                continue

            # Stream tokens via callback
            token_buffer = []

            def on_token(chunk: str):
                token_buffer.append(chunk)
                # Send each chunk via asyncio (from sync thread)
                asyncio.run_coroutine_threadsafe(
                    websocket.send_json({"chunk": chunk}),
                    asyncio.get_event_loop(),
                )

            # Run agent in thread pool (blocking), streaming via callback
            await _run_in_thread(platform.chat, user_message)

            await websocket.send_json({
                "done": True,
                "session_id": session_id,
                "full_response": "".join(token_buffer),
            })

    except WebSocketDisconnect:
        pass


# ─────────────────────────────────────────────────────────────
# P2-002: MODEL COST ROUTING
# cheap model for routing, expensive model for research work
# ─────────────────────────────────────────────────────────────

MODEL_ROUTING = {
    # Routing / classification: simple task → cheap model
    "orchestrator_routing":   "claude-haiku-4-5",

    # Simple formatting tasks
    "apa_reference":          "claude-haiku-4-5",
    "thesis_reviewer":        "claude-sonnet-4-6",

    # Core research work: needs best model
    "literature_search":      "claude-opus-4-8",
    "synthesis":              "claude-opus-4-8",
    "gap_brainstorm":         "claude-opus-4-8",
    "experiment_design":      "claude-opus-4-8",
    "questionnaire_design":   "claude-sonnet-4-6",
    "code_execution":         "claude-sonnet-4-6",
    "analysis":               "claude-opus-4-8",
    "paper_writing":          "claude-opus-4-8",
    "publication":            "claude-sonnet-4-6",
}

ESTIMATED_COST_PER_INTERACTION = {
    # (input_tokens, output_tokens) estimates per agent call
    "claude-haiku-4-5":   (0.80 / 1e6, 4.0 / 1e6),   # $0.80/$4.00 per 1M tokens
    "claude-sonnet-4-6":  (3.0 / 1e6,  15.0 / 1e6),  # $3/$15
    "claude-opus-4-8":    (15.0 / 1e6, 75.0 / 1e6),  # $15/$75
}

# Apply model routing — add to each agent's __init__:
#
#   from aviation_research_platform.fixes.p2_fastapi_backend import MODEL_ROUTING
#   self.MODEL = MODEL_ROUTING.get(self.name, "claude-sonnet-4-6")
