"""AI 서비스로 넘길 records 프레임 구성과 confidence 산정."""
from sqlalchemy.orm import Session as OrmSession

from app.models import Record

HABIT_COLS = ["sleep_hours", "stress_level", "late_snack", "exercise_min", "cosmetic_changed"]

# 패턴 분석/시나리오/patternReady의 공통 최소 기록 일수. 한 곳에서만 정의한다.
MIN_RECORDS = 7


def load_session_records(db: OrmSession, session_id: int) -> list[Record]:
    """세션의 기록을 recorded_at 오름차순으로 로드한다(분석·목록 공통)."""
    return (
        db.query(Record)
        .filter(Record.session_id == session_id)
        .order_by(Record.recorded_at.asc())
        .all()
    )


def build_frame(records: list[Record]) -> list[dict]:
    """recorded_at 오름차순 기록을 AI 계약 형태의 dict 리스트로 변환."""
    return [
        {
            "recorded_at": r.recorded_at.isoformat(),
            "sleep_hours": r.sleep_hours,
            "stress_level": r.stress_level,
            "late_snack": r.late_snack,
            "exercise_min": r.exercise_min,
            "cosmetic_changed": r.cosmetic_changed,
            "skin_score": r.skin_score,
        }
        for r in records
    ]


def confidence_for(n: int) -> str | None:
    if n >= 21:
        return "high"
    if n >= 14:
        return "medium"
    if n >= 7:
        return "low"
    return None
