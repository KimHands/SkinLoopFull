from fastapi import APIRouter, Depends
from pydantic import ValidationError
from sqlalchemy.orm import Session as OrmSession

from app.analysis import engine
from app.analysis.fallback import fallback
from app.analysis.frame import MIN_RECORDS, build_frame, confidence_for, load_session_records
from app.db import get_db
from app.deps import require_session
from app.models import Session as SessionModel
from app.schemas import PatternResponse

router = APIRouter(prefix="/api", tags=["patterns"])


def _fallback_response(n: int) -> PatternResponse:
    """AI 서비스 불가/응답 이상 시 impacts 없이 규칙 문장만. 화면이 비지 않게 한다."""
    fb = fallback([])
    return PatternResponse(
        confidence=confidence_for(n),
        record_days=n,
        impacts=[],
        insight=fb["insight"],
        is_fallback=True,
    )


@router.get("/patterns", response_model=PatternResponse)
def get_patterns(
    session: SessionModel = Depends(require_session),
    db: OrmSession = Depends(get_db),
):
    """패턴 분석. <7일이면 기록부족, AI 서비스 실패·응답 이상 시 규칙 폴백."""
    records = load_session_records(db, session.id)
    n = len(records)

    if n < MIN_RECORDS:
        need = MIN_RECORDS - n
        return PatternResponse(
            confidence=None,
            record_days=n,
            impacts=[],
            insight=None,
            reason="NOT_ENOUGH_RECORDS",
            need_more=need,
            message=f"앞으로 {need}일 더 기록하면 패턴 분석이 시작됩니다.",
        )

    try:
        result = engine.fetch_patterns(build_frame(records))
    except engine.AIServiceUnavailable:
        return _fallback_response(n)

    try:
        result.setdefault("record_days", n)
        return PatternResponse(**result)
    except (ValidationError, TypeError, AttributeError):
        # AI Repo와 스키마가 어긋난 응답 → 폴백으로 degrade(500 금지)
        return _fallback_response(n)
