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
