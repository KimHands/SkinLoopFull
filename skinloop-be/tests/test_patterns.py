import pytest

from app.analysis import engine


def _h(token):
    return {"X-Anon-Token": token}


def _rec(date_str):
    return {
        "recordedAt": date_str,
        "sleepHours": 6.0,
        "lateSnack": False,
        "stressLevel": 2,
        "exerciseMin": 20,
        "cosmeticChanged": False,
        "skinRedness": 2,
        "skinAcneCount": 2,
        "skinOiliness": 2,
    }


def _seed_records(client, token, n):
    for day in range(1, n + 1):
        client.post("/api/records", json=_rec(f"2026-08-{day:02d}"), headers=_h(token))


AI_PATTERN = {
    "confidence": "high",
    "record_days": 7,
    "impacts": [
        {"factor": "sleep_short", "label": "6시간 미만 수면", "impact": 0.42, "lag": 1, "corr": 0.61},
        {"factor": "late_snack", "label": "야식", "impact": 0.31, "lag": 1, "corr": 0.48},
        {"factor": "stress", "label": "스트레스", "impact": 0.14, "lag": 0, "corr": 0.22},
    ],
    "insight": "6시간 미만 수면이 다음 날 피부와 가장 높은 연관을 보였습니다.",
    "evidence_dates": ["2026-08-01", "2026-08-02", "2026-08-03"],
    "suggested_experiment": {"target_habit": "sleep_short", "title": "취침 40분 앞당기기", "duration_days": 14},
    "is_fallback": False,
    "model_version": "habitpattern-v1.0",
}


def test_not_enough_records_returns_reason(client, session_token):
    _seed_records(client, session_token, 3)
    resp = client.get("/api/patterns", headers=_h(session_token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["reason"] == "NOT_ENOUGH_RECORDS"
    assert body["needMore"] == 4
    assert body["confidence"] is None
    assert body["impacts"] == []


def test_returns_ai_impacts_when_service_ok(client, session_token, monkeypatch):
    _seed_records(client, session_token, 7)
    monkeypatch.setattr(engine, "fetch_patterns", lambda records: dict(AI_PATTERN))
    resp = client.get("/api/patterns", headers=_h(session_token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["isFallback"] is False
    assert [i["factor"] for i in body["impacts"]] == ["sleep_short", "late_snack", "stress"]
    assert body["confidence"] == "high"


def test_falls_back_when_ai_unavailable(client, session_token, monkeypatch):
    _seed_records(client, session_token, 14)

    def _boom(records):
        raise engine.AIServiceUnavailable("down")

    monkeypatch.setattr(engine, "fetch_patterns", _boom)
    resp = client.get("/api/patterns", headers=_h(session_token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["isFallback"] is True
    assert body["insight"]  # 폴백 문장은 반드시 있어야 한다
    assert body["confidence"] == "medium"  # 14일 → medium (로컬 계산)
    assert body["recordDays"] == 14


def test_malformed_ai_response_falls_back_not_500(client, session_token, monkeypatch):
    # AI Repo가 계약과 다른 factor 이름을 반환(스키마 드리프트) → 폴백해야지 500 나면 안 됨
    _seed_records(client, session_token, 7)
    bad = {"confidence": "high", "impacts": [{"factor": "sleep", "label": "x", "impact": 0.4, "lag": 1, "corr": 0.5}]}
    monkeypatch.setattr(engine, "fetch_patterns", lambda records: dict(bad))
    resp = client.get("/api/patterns", headers=_h(session_token))
    assert resp.status_code == 200
    assert resp.json()["isFallback"] is True


def test_patterns_missing_token_401(client):
    resp = client.get("/api/patterns")
    assert resp.status_code == 401
