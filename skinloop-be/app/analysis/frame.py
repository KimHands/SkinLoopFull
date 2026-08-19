"""records 로딩·최소 기록 일수 공통 헬퍼 (session/records 라우터가 공유)."""
from sqlalchemy.orm import Session as OrmSession

from app.models import Record

# patternReady 판정 등 최소 기록 일수. 한 곳에서만 정의한다.
MIN_RECORDS = 7


def load_session_records(db: OrmSession, session_id: int) -> list[Record]:
    """세션의 기록을 recorded_at 오름차순으로 로드한다."""
    return (
        db.query(Record)
        .filter(Record.session_id == session_id)
        .order_by(Record.recorded_at.asc())
        .all()
    )


def session_ai_records(db: OrmSession, session_id: int) -> list[dict]:
    """세션 기록을 AI 모듈 입력 dict(오름차순)으로 변환한다.

    patterns/whatif가 공유. 프론트가 records를 body로 보내는 대신 DB에서 조회한다.
    """
    return [
        {
            "recorded_at": r.recorded_at.isoformat(),
            "sleep_hours": r.sleep_hours,
            "late_snack": r.late_snack,
            "stress_level": r.stress_level,
            "exercise_min": r.exercise_min,
            "cosmetic_changed": r.cosmetic_changed,
            "skin_score": r.skin_score,
        }
        for r in load_session_records(db, session_id)
    ]
