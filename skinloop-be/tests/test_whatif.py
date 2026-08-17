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


def _seed(client, token, n):
    for day in range(1, n + 1):
        client.post("/api/records", json=_rec(f"2026-08-{day:02d}"), headers=_h(token))


AI_WHATIF = {
    "target_habit": "sleep_short",
    "current": {"label": "현재 습관 유지", "range": {"min": 52, "max": 58}, "trend": [54, 54, 53, 55]},
    "changed": {"label": "습관 변경 적용", "range": {"min": 60, "max": 66}, "trend": [55, 58, 61, 63]},
    "direction": "improve",
    "confidence": "medium",
    "disclaimer": "예측이 아닌 시나리오 비교이며, 실제 결과는 다를 수 있습니다.",
}


def test_returns_range_and_direction(client, session_token, monkeypatch):
    _seed(client, session_token, 7)
    monkeypatch.setattr(engine, "fetch_whatif", lambda *a, **k: dict(AI_WHATIF))
    resp = client.post(
        "/api/whatif",
        json={"targetHabit": "sleep_short", "changeValue": 1.0},
        headers=_h(session_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["direction"] == "improve"
    assert body["current"]["range"] == {"min": 52, "max": 58}
    assert body["changed"]["range"] == {"min": 60, "max": 66}
    assert len(body["changed"]["trend"]) == 4
    assert body["label"]  # BE가 구성한 사람 읽는 라벨
    assert body["message"]
    assert body["disclaimer"]


def test_not_enough_records_returns_400(client, session_token):
    _seed(client, session_token, 3)
    resp = client.post(
        "/api/whatif",
        json={"targetHabit": "sleep_short", "changeValue": 1.0},
        headers=_h(session_token),
    )
    assert resp.status_code == 400
    assert resp.json()["error"] == "NOT_ENOUGH_RECORDS"


def test_ai_unavailable_returns_503(client, session_token, monkeypatch):
    _seed(client, session_token, 7)

    def _boom(*a, **k):
        raise engine.AIServiceUnavailable("down")

    monkeypatch.setattr(engine, "fetch_whatif", _boom)
    resp = client.post(
        "/api/whatif",
        json={"targetHabit": "sleep_short", "changeValue": 1.0},
        headers=_h(session_token),
    )
    assert resp.status_code == 503


def test_malformed_ai_response_returns_503_not_500(client, session_token, monkeypatch):
    # AI가 200이지만 계약 키 누락(부분 응답) → 503으로 degrade, 500 나면 안 됨
    _seed(client, session_token, 7)
    monkeypatch.setattr(engine, "fetch_whatif", lambda *a, **k: {"direction": "improve"})
    resp = client.post(
        "/api/whatif",
        json={"targetHabit": "sleep_short", "changeValue": 1.0},
        headers=_h(session_token),
    )
    assert resp.status_code == 503


def test_whatif_missing_token_401(client):
    resp = client.post("/api/whatif", json={"targetHabit": "sleep_short", "changeValue": 1.0})
    assert resp.status_code == 401
