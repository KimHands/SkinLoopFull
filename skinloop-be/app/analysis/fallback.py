"""규칙 기반 폴백 문장 (spec §6 / docs/spec/05-ai-module).

LLM/AI 서비스가 실패해도 화면이 비지 않도록 문장·실험을 규칙으로 채운다.
impacts가 있으면 1위 요인 기준 문장을, 없으면(=서비스 전체 불가) 중립 문장을 쓴다.
표현 규칙(08-conventions): '원인' 금지 → '연관'.
"""

FALLBACK_INSIGHT = {
    "sleep_short": "6시간 미만 수면이 다음 날 피부 상태와 가장 높은 연관을 보였습니다.",
    "late_snack": "야식이 다음 날 피부 상태와 높은 연관을 보였습니다.",
    "stress": "스트레스가 높았던 날 피부 상태가 낮게 기록되었습니다.",
    "exercise": "운동량과 피부 상태 사이에 일정한 경향이 나타났습니다.",
    "cosmetic_changed": "화장품 변경 시점과 피부 변화가 함께 나타났습니다.",
}

FALLBACK_EXPERIMENT = {
    "sleep_short": ("취침 시간 40분 앞당기기", 14),
    "late_snack": ("야식 주 2회 이하로 줄이기", 14),
    "stress": ("취침 전 10분 이완 루틴", 14),
    "exercise": ("주 3회 20분 걷기", 14),
    "cosmetic_changed": ("2주간 화장품 변경 없이 유지하기", 14),
}

_NO_IMPACT_INSIGHT = "지금은 분석 문장을 불러오지 못했습니다. 기록이 쌓일수록 더 정확한 패턴을 볼 수 있어요."


def fallback(impacts: list[dict]) -> dict:
    """impacts를 유지한 채 문장만 규칙 기반으로 채운다."""
    if not impacts:
        return {"insight": _NO_IMPACT_INSIGHT, "is_fallback": True}
    top = impacts[0]["factor"]
    title, days = FALLBACK_EXPERIMENT.get(top, ("생활습관 하나 바꿔보기", 14))
    return {
        "insight": FALLBACK_INSIGHT.get(top, "기록에서 일정한 경향이 나타났습니다."),
        "suggested_experiment": {"target_habit": top, "title": title, "duration_days": days},
        "is_fallback": True,
    }
