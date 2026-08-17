from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session as OrmSession

from app.analysis import engine
from app.analysis.frame import MIN_RECORDS, build_frame, load_session_records
from app.db import get_db
from app.deps import require_session
from app.models import Session as SessionModel
from app.schemas import WhatIfRequest, WhatIfResponse

router = APIRouter(prefix="/api", tags=["whatif"])


def _fmt(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


def _label(target_habit: str, change_value: float) -> str:
    v = _fmt(change_value)
    return {
        "sleep_short": f"수면 +{v}시간",
        "late_snack": f"야식 주 {v}회 줄이기",
        "stress": f"스트레스 {v}단계 낮추기",
        "exercise": f"운동 +{v}분",
    }.get(target_habit, "습관 변경")


def _message(label: str, direction: str) -> str:
    # 표현 규칙(08): 점 추정치·단정 금지, '예측'이 아닌 '유사한 패턴'.
    if direction == "improve":
        return f"{label}한 경우, 지금까지 기록에서 좋았던 날들과 유사한 패턴을 보입니다."
    if direction == "worsen":
        return f"{label}한 경우, 기록에서 낮았던 날들과 유사한 패턴을 보입니다."
    return f"{label}한 경우, 뚜렷한 차이는 나타나지 않았습니다."


def _service_unavailable() -> HTTPException:
    return HTTPException(
        status_code=503,
        detail={"error": "AI_UNAVAILABLE", "message": "분석 서비스를 잠시 사용할 수 없습니다"},
    )


@router.post("/whatif", response_model=WhatIfResponse)
def post_whatif(
    payload: WhatIfRequest,
    session: SessionModel = Depends(require_session),
    db: OrmSession = Depends(get_db),
):
    """습관 하나를 바꿨을 때의 시나리오 비교. 항상 range로 응답(점추정 금지)."""
    records = load_session_records(db, session.id)
    if len(records) < MIN_RECORDS:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "NOT_ENOUGH_RECORDS",
                "message": f"시나리오 비교에는 최소 {MIN_RECORDS}일치 기록이 필요합니다",
            },
        )

    try:
        result = engine.fetch_whatif(
            build_frame(records), payload.target_habit, payload.change_value
        )
    except engine.AIServiceUnavailable:
        raise _service_unavailable()

    label = _label(payload.target_habit, payload.change_value)
    try:
        return WhatIfResponse(
            target_habit=payload.target_habit,
            label=label,
            current=result["current"],
            changed=result["changed"],
            direction=result["direction"],
            confidence=result["confidence"],
            message=_message(label, result["direction"]),
            disclaimer=result.get(
                "disclaimer", "예측이 아닌 시나리오 비교이며, 실제 결과는 다를 수 있습니다."
            ),
        )
    except (KeyError, TypeError, ValidationError):
        # AI 응답이 계약과 어긋남 → 503으로 degrade(500 금지). 점추정 응답을 만들지 않는다.
        raise _service_unavailable()
