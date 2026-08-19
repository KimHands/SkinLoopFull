from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.analysis.frame import session_ai_records
from app.db import get_db
from app.deps import require_session
from app.models import Session as SessionModel
from app.schemas import ErrorResponse

router = APIRouter(prefix="/api", tags=["patterns"])


def _ai_unavailable(detail: str) -> HTTPException:
    return HTTPException(
        status_code=503,
        detail=ErrorResponse(error="AI_UNAVAILABLE", detail=detail).model_dump(),
    )


@router.get("/patterns")
def get_patterns(
    session: SessionModel = Depends(require_session),
    db: OrmSession = Depends(get_db),
):
    """세션 기록으로 패턴 분석. 응답은 명세(03-types PatternResponse) 평면 형태."""
    # AI 모듈(src.*)·LLM 문장화는 AI Repo 소유. 미설치 환경에서도 앱이 부팅되도록 지연 import.
    try:
        from src.habit_pattern import analyze_patterns

        from app.llm_formatter import summarize_habit_pattern
    except ImportError as exc:
        raise _ai_unavailable(str(exc))

    records = session_ai_records(db, session.id)
    try:
        result = analyze_patterns(records)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(error="INVALID_INPUT", detail=str(exc)).model_dump(),
        )

    # 문장화는 통계 결과(impacts)가 있을 때만. insight가 비어 있으면 채운다.
    if result.get("impacts") and not result.get("insight"):
        result["insight"] = summarize_habit_pattern(result)

    return result
