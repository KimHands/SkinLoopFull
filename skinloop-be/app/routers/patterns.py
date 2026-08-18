from fastapi import APIRouter, HTTPException

from app.schemas import ErrorResponse, RecordsPayload

router = APIRouter(prefix="/api", tags=["patterns"])


def _ai_unavailable(detail: str) -> HTTPException:
    return HTTPException(
        status_code=503,
        detail=ErrorResponse(error="AI_UNAVAILABLE", detail=detail).model_dump(),
    )


@router.post("/patterns")
def get_patterns(payload: RecordsPayload):
    # AI 모듈(src.*)·LLM 문장화는 AI Repo 소유. 미설치 환경에서도 앱이 부팅되도록 지연 import.
    try:
        from src.habit_pattern import analyze_patterns

        from app.llm_formatter import summarize_habit_pattern
    except ImportError as exc:
        raise _ai_unavailable(str(exc))

    try:
        records = payload.sorted_ai_records()
        result = analyze_patterns(records)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(error="INVALID_INPUT", detail=str(exc)).model_dump(),
        )

    narrative = None
    if result.get("recordDays") is not None and "impacts" in result:
        narrative = summarize_habit_pattern(result)

    return {"result": result, "narrative": narrative}
