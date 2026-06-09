"""
P2-003 FIX: Database-backed Session Storage
=============================================
แทนที่ JSON files ด้วย SQLite (dev) หรือ PostgreSQL (prod)
Install: pip install sqlalchemy aiosqlite (dev) หรือ asyncpg (prod)
"""
from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, DateTime, create_engine, Index
)
from sqlalchemy.orm import DeclarativeBase, Session as DBSession, sessionmaker


class Base(DeclarativeBase):
    pass


class ResearchSessionRecord(Base):
    """ORM model for research session persistence."""

    __tablename__ = "research_sessions"

    session_id        = Column(String(16), primary_key=True)
    user_id           = Column(String(64), nullable=True, index=True)  # for multi-user
    research_question = Column(Text, nullable=False)
    domain            = Column(String(200), nullable=False)
    current_phase     = Column(String(50), default="discovery")
    artifacts_json    = Column(Text, default="[]")    # JSON array
    hypotheses_json   = Column(Text, default="[]")
    dead_ends_json    = Column(Text, default="[]")
    notes_json        = Column(Text, default="[]")
    created_at        = Column(DateTime, default=datetime.utcnow)
    updated_at        = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_session_user_updated", "user_id", "updated_at"),
    )


class SessionRepository:
    """
    Replaces the JSON file persistence in ResearchSession.
    Supports SQLite (dev) and PostgreSQL (prod) via SQLAlchemy.
    """

    def __init__(self, database_url: str = "sqlite:///./research_os.db"):
        # Dev:  "sqlite:///./research_os.db"
        # Prod: "postgresql+asyncpg://user:pass@host/dbname"
        self.engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save(self, session) -> None:
        """Persist a ResearchSession object."""
        from aviation_research_platform.core.session import ResearchSession
        from dataclasses import asdict

        with self.Session() as db:
            record = db.get(ResearchSessionRecord, session.session_id)
            if not record:
                record = ResearchSessionRecord(session_id=session.session_id)
                db.add(record)

            record.research_question = session.research_question
            record.domain            = session.domain
            record.current_phase     = session.current_phase.value
            record.artifacts_json    = json.dumps(
                [asdict(a) for a in session.artifacts], default=str
            )
            record.hypotheses_json   = json.dumps(session.hypotheses)
            record.dead_ends_json    = json.dumps(session.dead_ends)
            record.notes_json        = json.dumps(session.notes)
            record.updated_at        = datetime.utcnow()
            db.commit()

    def load(self, session_id: str):
        """Load and return a ResearchSession object."""
        from aviation_research_platform.core.session import (
            ResearchSession, ResearchPhase, PhaseArtifact
        )
        with self.Session() as db:
            record = db.get(ResearchSessionRecord, session_id)
            if not record:
                raise FileNotFoundError(f"Session {session_id} not found")

            artifacts_data = json.loads(record.artifacts_json or "[]")

            session = ResearchSession(
                session_id=record.session_id,
                research_question=record.research_question,
                domain=record.domain,
                current_phase=ResearchPhase(record.current_phase),
                artifacts=[PhaseArtifact(**a) for a in artifacts_data],
                hypotheses=json.loads(record.hypotheses_json or "[]"),
                dead_ends=json.loads(record.dead_ends_json or "[]"),
                notes=json.loads(record.notes_json or "[]"),
            )
            return session

    def list_by_user(self, user_id: str, limit: int = 20) -> list[dict]:
        with self.Session() as db:
            records = (
                db.query(ResearchSessionRecord)
                .filter(ResearchSessionRecord.user_id == user_id)
                .order_by(ResearchSessionRecord.updated_at.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "session_id": r.session_id,
                    "research_question": r.research_question[:80],
                    "current_phase": r.current_phase,
                    "updated_at": r.updated_at.isoformat(),
                }
                for r in records
            ]

    def delete(self, session_id: str) -> None:
        with self.Session() as db:
            record = db.get(ResearchSessionRecord, session_id)
            if record:
                db.delete(record)
                db.commit()


# ── HOW TO WIRE INTO ResearchSession ────────────────────────────────────

INTEGRATION_EXAMPLE = """
# In core/session.py — replace save/load with repository calls:

# At module level:
_repo = SessionRepository()  # uses SQLite by default

# In ResearchSession:
def save(self, store_dir=None):
    _repo.save(self)

@classmethod
def load(cls, session_id, store_dir=None):
    return _repo.load(session_id)
"""
