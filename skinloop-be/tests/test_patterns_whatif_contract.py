"""patterns/whatif 라우터 계약 회귀 테스트 (명세 04-api 준수).

AI 모듈(src.*)은 이 레포에 없으므로 실제 분석 결과는 검증할 수 없다.
여기서는 명세가 정한 계약만 고정한다:
- patterns는 GET, whatif 입력은 {targetHabit, changeValue}이며 records를 body로 받지 않는다.
- 인증 헤더 누락은 401.
- AI 모듈 미설치 시 503 AI_UNAVAILABLE로 수렴(라우터·세션·DB 조회까지 정상 도달했다는 뜻).
"""

HEADERS = lambda token: {"X-Anon-Token": token}


def test_patterns_is_get(client):
    # POST는 더 이상 허용되지 않는다(405).
    assert client.post("/api/patterns").status_code == 405


def test_patterns_missing_token_returns_401(client):
    assert client.get("/api/patterns").status_code == 401


def test_patterns_reaches_ai_boundary(client, session_token):
    # 세션·DB 조회를 통과하면 AI 미설치라 503 AI_UNAVAILABLE.
    resp = client.get("/api/patterns", headers=HEADERS(session_token))
    assert resp.status_code == 503
    assert resp.json()["error"] == "AI_UNAVAILABLE"


def test_whatif_missing_token_returns_401(client):
    resp = client.post("/api/whatif", json={"targetHabit": "sleep_short", "changeValue": 1})
    assert resp.status_code == 401


def test_whatif_requires_no_records_in_body(client, session_token):
    # records 없이도 검증을 통과해 AI 경계(503)까지 도달한다.
    resp = client.post(
        "/api/whatif",
        json={"targetHabit": "sleep_short", "changeValue": 1},
        headers=HEADERS(session_token),
    )
    assert resp.status_code == 503
    assert resp.json()["error"] == "AI_UNAVAILABLE"


def test_whatif_missing_target_returns_400(client, session_token):
    resp = client.post(
        "/api/whatif",
        json={"changeValue": 1},
        headers=HEADERS(session_token),
    )
    assert resp.status_code == 400
    assert resp.json()["error"].startswith("INVALID_")


def test_whatif_rejects_unknown_target(client, session_token):
    resp = client.post(
        "/api/whatif",
        json={"targetHabit": "cosmetic_changed", "changeValue": 1},
        headers=HEADERS(session_token),
    )
    assert resp.status_code == 400
