from fastapi import APIRouter, HTTPException

from app.schemas import ErrorResponse, WhatIfRequest

router = APIRouter(prefix="/api", tags=["whatif"])


def _ai_unavailable(detail: str) -> HTTPException:
    return HTTPException(
        status_code=503,
        detail=ErrorResponse(error="AI_UNAVAILABLE", detail=detail).model_dump(),
    )


@router.post("/whatif")
def post_whatif(payload: WhatIfRequest):
    # AI 모듈(src.*)·LLM 문장화는 AI Repo 소유. 미설치 환경에서도 앱이 부팅되도록 지연 import.
    try:
        from src.whatif import run_whatif

        from app.llm_formatter import summarize_whatif
    except ImportError as exc:
        raise _ai_unavailable(str(exc))

    try:
        records = payload.sorted_ai_records()
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

    narrative = summarize_whatif(result)
    return {"result": result, "narrative": narrative}
