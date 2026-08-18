from fastapi import APIRouter, HTTPException

from src.habit_pattern import analyze_patterns

from app.schemas import RecordsPayload, ErrorResponse
from app.llm_formatter import summarize_habit_pattern

router = APIRouter(prefix="/api", tags=["patterns"])


@router.post("/patterns")
def get_patterns(payload: RecordsPayload):
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