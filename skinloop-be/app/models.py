"""SQLAlchemy 모델 (spec §3 / docs/spec/02-data-model).

테이블 4개: sessions, records, analyses, experiments.
포터블 타입만 사용 — SQLite(로컬)와 Postgres(배포) 양쪽에 매핑된다.
web.md 규칙: 프로덕션 스키마 생성·변경은 사람이 한다.
"""
from datetime import date, datetime, timezone

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    anon_token: Mapped[str] = mapped_column(String(36), unique=True, nullable=False, index=True)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    records: Mapped[list["Record"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    experiments: Mapped[list["Experiment"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class Record(Base):
    __tablename__ = "records"
    __table_args__ = (UniqueConstraint("session_id", "recorded_at", name="uq_records_session_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False, index=True)
    recorded_at: Mapped[date] = mapped_column(Date, nullable=False)

    sleep_hours: Mapped[float] = mapped_column(Float, nullable=False)
    late_snack: Mapped[bool] = mapped_column(Boolean, nullable=False)
    stress_level: Mapped[int] = mapped_column(Integer, nullable=False)
    exercise_min: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cosmetic_changed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    skin_redness: Mapped[int] = mapped_column(Integer, nullable=False)
    skin_acne_count: Mapped[int] = mapped_column(Integer, nullable=False)
    skin_oiliness: Mapped[int] = mapped_column(Integer, nullable=False)
    skin_score: Mapped[int] = mapped_column(Integer, nullable=False)
    memo: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    session: Mapped["Session"] = relationship(back_populates="records")


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False, index=True)
    impacts: Mapped[list | None] = mapped_column(JSON, nullable=True)
    insight: Mapped[str | None] = mapped_column(String, nullable=True)
    confidence: Mapped[str | None] = mapped_column(String(10), nullable=True)
    evidence_dates: Mapped[list | None] = mapped_column(JSON, nullable=True)
    record_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_fallback: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    model_version: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False, index=True)
    target_habit: Mapped[str] = mapped_column(String(30), nullable=False)
    title: Mapped[str | None] = mapped_column(String(100), nullable=True)
    duration_days: Mapped[int] = mapped_column(Integer, default=14)
    status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    baseline_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    result_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    verdict: Mapped[str | None] = mapped_column(String(20), nullable=True)
    started_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    ended_at: Mapped[date | None] = mapped_column(Date, nullable=True)

    session: Mapped["Session"] = relationship(back_populates="experiments")
