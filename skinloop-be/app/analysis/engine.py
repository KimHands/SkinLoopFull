"""AI 분석 엔진 HTTP 클라이언트 (BE ↔ AI Repo 계약, open-questions A1).

통계 엔진(habit_pattern·whatif)은 AI Repo가 별도 HTTP 서비스로 제공한다.
BE는 records를 넘기고 결과 dict를 받는다. 서비스 미설정/불가/타임아웃이면
AIServiceUnavailable을 던져 라우터가 폴백하게 한다.

AI 서비스 계약(AI Repo가 구현):
    POST {AI_SERVICE_URL}/patterns
        body: {"records": [ {recorded_at, sleep_hours, stress_level, late_snack,
                             exercise_min, cosmetic_changed, skin_score}, ... ]}
        200:  PatternResponse dict (impacts, insight, confidence, evidence_dates,
              suggested_experiment, is_fallback, model_version)
    POST {AI_SERVICE_URL}/whatif
        body: {"records": [...], "target_habit": str, "change_value": float}
        200:  WhatIfResult dict (current, changed, direction, confidence, ...)
"""
import httpx

from app.config import AI_SERVICE_URL, AI_TIMEOUT_SECONDS


class AIServiceUnavailable(Exception):
    """AI 분석 서비스에 도달할 수 없거나 오류를 반환했을 때."""


def _post(path: str, body: dict) -> dict:
    if not AI_SERVICE_URL:
        raise AIServiceUnavailable("AI_SERVICE_URL 미설정")
    url = f"{AI_SERVICE_URL.rstrip('/')}{path}"
    try:
        resp = httpx.post(url, json=body, timeout=AI_TIMEOUT_SECONDS)
        resp.raise_for_status()
        return resp.json()
    except (httpx.HTTPError, ValueError) as exc:  # 연결/타임아웃/HTTP오류/JSON파싱
        raise AIServiceUnavailable(str(exc)) from exc


def fetch_patterns(records: list[dict]) -> dict:
    return _post("/patterns", {"records": records})


def fetch_whatif(records: list[dict], target_habit: str, change_value: float) -> dict:
    return _post(
        "/whatif",
        {"records": records, "target_habit": target_habit, "change_value": change_value},
    )
