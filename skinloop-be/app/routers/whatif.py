from fastapi import APIRouter, HTTPException

from src.whatif import run_whatif

from app.schemas import WhatIfRequest, ErrorResponse
from app.llm_formatter import summarize_whatif

router = APIRouter(prefix="/api", tags=["whatif"])


@router.post("/whatif")
def post_whatif(payload: WhatIfRequest):
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