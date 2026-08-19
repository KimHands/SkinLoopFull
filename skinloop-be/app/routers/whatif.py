from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.analysis.frame import session_ai_records
from app.db import get_db
from app.deps import require_session
from app.models import Session as SessionModel
from app.schemas import ErrorResponse, WhatIfRequest

router = APIRouter(prefix="/api", tags=["whatif"])

DISCLAIMER = "본 분석은 통계적 연관성을 보여주는 참고 자료이며 의학적 진단이 아닙니다."


def _ai_unavailable(detail: str) -> HTTPException:
    return HTTPException(
        status_code=503,
        detail=ErrorResponse(error="AI_UNAVAILABLE", detail=detail).model_dump(),
    )


@router.post("/whatif")
def post_whatif(
    payload: WhatIfRequest,
    session: SessionModel = Depends(require_session),
    db: OrmSession = Depends(get_db),
):
    """세션 기록으로 시나리오 비교. 응답은 명세(03-types WhatIfResponse) 평면 형태."""
    # AI 모듈(src.*)·LLM 문장화는 AI Repo 소유. 미설치 환경에서도 앱이 부팅되도록 지연 import.
    try:
        from src.whatif import run_whatif

        from app.llm_formatter import summarize_whatif
    except ImportError as exc:
        raise _ai_unavailable(str(exc))

    records = session_ai_records(db, session.id)
    try:
        result = run_whatif(
            records=records,
            target_habit=payload.target_habit,
            change_value=payload.change_value,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(error="INVALID_INPUT", detail=str(exc)).model_dump(),
        )

    if not result.get("message"):
        result["message"] = summarize_whatif(result)
    result.setdefault("disclaimer", DISCLAIMER)

    return result
